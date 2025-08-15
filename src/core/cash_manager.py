
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cash and Transfer Manager
مدير الكاش والتحويلات
"""

from datetime import datetime, date
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import sqlite3

from src.utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class CashTransaction:
    """Cash transaction data model"""
    id: Optional[int] = None
    transaction_type: str = ""  # 'in', 'out', 'transfer'
    amount: float = 0.0
    from_method: Optional[str] = None
    to_method: Optional[str] = None
    description: str = ""
    reference_id: Optional[int] = None
    reference_type: Optional[str] = None
    created_by: str = ""
    created_at: Optional[str] = None

@dataclass
class DailyCashSummary:
    """Daily cash summary data model"""
    id: Optional[int] = None
    date: str = ""
    opening_balance: float = 0.0
    total_cash_in: float = 0.0
    total_cash_out: float = 0.0
    total_transfers_in: float = 0.0
    total_transfers_out: float = 0.0
    closing_balance: float = 0.0
    notes: str = ""
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class CashManager:
    """Manager for cash transactions and transfers"""

    def __init__(self, db_manager):
        """Initialize cash manager"""
        self.db_manager = db_manager
        logger.info("Cash manager initialized")

    def add_cash_transaction(self, transaction: CashTransaction) -> bool:
        """Add a cash transaction"""
        try:
            cursor = self.db_manager.connection.cursor()
            
            cursor.execute('''
                INSERT INTO cash_transactions 
                (transaction_type, amount, from_method, to_method, description, 
                 reference_id, reference_type, created_by, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                transaction.transaction_type,
                transaction.amount,
                transaction.from_method,
                transaction.to_method,
                transaction.description,
                transaction.reference_id,
                transaction.reference_type,
                transaction.created_by,
                transaction.created_at or datetime.now().isoformat()
            ))
            
            self.db_manager.connection.commit()
            
            # Update daily summary
            self._update_daily_summary(date.today().isoformat())
            
            logger.info(f"Cash transaction added: {transaction.transaction_type} - {transaction.amount}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding cash transaction: {e}")
            self.db_manager.connection.rollback()
            return False

    def record_sale_payment(self, sale_id: int, amount: float, payment_method: str) -> bool:
        """Record payment for a sale"""
        transaction = CashTransaction(
            transaction_type="in",
            amount=amount,
            to_method=payment_method,
            description=f"Payment for sale #{sale_id}",
            reference_id=sale_id,
            reference_type="sale",
            created_by="system"
        )
        return self.add_cash_transaction(transaction)

    def record_expense(self, amount: float, payment_method: str, description: str, expense_id: int = None) -> bool:
        """Record an expense"""
        transaction = CashTransaction(
            transaction_type="out",
            amount=amount,
            from_method=payment_method,
            description=description,
            reference_id=expense_id,
            reference_type="expense",
            created_by="system"
        )
        return self.add_cash_transaction(transaction)

    def record_transfer(self, amount: float, from_method: str, to_method: str, description: str) -> bool:
        """Record a transfer between payment methods"""
        transaction = CashTransaction(
            transaction_type="transfer",
            amount=amount,
            from_method=from_method,
            to_method=to_method,
            description=description,
            reference_type="transfer",
            created_by="user"
        )
        return self.add_cash_transaction(transaction)

    def get_cash_balance(self, payment_method: str = "cash") -> float:
        """Get current balance for a payment method"""
        try:
            cursor = self.db_manager.connection.cursor()
            
            # Calculate total in
            cursor.execute('''
                SELECT COALESCE(SUM(amount), 0) 
                FROM cash_transactions 
                WHERE (transaction_type = 'in' AND to_method = ?) 
                   OR (transaction_type = 'transfer' AND to_method = ?)
            ''', (payment_method, payment_method))
            
            total_in = cursor.fetchone()[0]
            
            # Calculate total out
            cursor.execute('''
                SELECT COALESCE(SUM(amount), 0) 
                FROM cash_transactions 
                WHERE (transaction_type = 'out' AND from_method = ?) 
                   OR (transaction_type = 'transfer' AND from_method = ?)
            ''', (payment_method, payment_method))
            
            total_out = cursor.fetchone()[0]
            
            return total_in - total_out
            
        except Exception as e:
            logger.error(f"Error getting cash balance: {e}")
            return 0.0

    def get_daily_transactions(self, target_date: str = None) -> List[CashTransaction]:
        """Get transactions for a specific date"""
        try:
            if not target_date:
                target_date = date.today().isoformat()
            
            cursor = self.db_manager.connection.cursor()
            cursor.execute('''
                SELECT id, transaction_type, amount, from_method, to_method, 
                       description, reference_id, reference_type, created_by, created_at
                FROM cash_transactions 
                WHERE DATE(created_at) = ?
                ORDER BY created_at DESC
            ''', (target_date,))
            
            transactions = []
            for row in cursor.fetchall():
                transaction = CashTransaction(
                    id=row[0],
                    transaction_type=row[1],
                    amount=row[2],
                    from_method=row[3],
                    to_method=row[4],
                    description=row[5],
                    reference_id=row[6],
                    reference_type=row[7],
                    created_by=row[8],
                    created_at=row[9]
                )
                transactions.append(transaction)
            
            return transactions
            
        except Exception as e:
            logger.error(f"Error getting daily transactions: {e}")
            return []

    def get_payment_method_summary(self) -> Dict[str, float]:
        """Get balance summary for all payment methods"""
        try:
            cursor = self.db_manager.connection.cursor()
            cursor.execute('SELECT name FROM payment_methods WHERE is_active = 1')
            
            summary = {}
            for (method_name,) in cursor.fetchall():
                balance = self.get_cash_balance(method_name)
                summary[method_name] = balance
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting payment method summary: {e}")
            return {}

    def _update_daily_summary(self, target_date: str):
        """Update daily cash summary"""
        try:
            cursor = self.db_manager.connection.cursor()
            
            # Calculate totals for the day
            cursor.execute('''
                SELECT 
                    COALESCE(SUM(CASE WHEN transaction_type = 'in' THEN amount ELSE 0 END), 0) as cash_in,
                    COALESCE(SUM(CASE WHEN transaction_type = 'out' THEN amount ELSE 0 END), 0) as cash_out,
                    COALESCE(SUM(CASE WHEN transaction_type = 'transfer' AND to_method = 'cash' THEN amount ELSE 0 END), 0) as transfer_in,
                    COALESCE(SUM(CASE WHEN transaction_type = 'transfer' AND from_method = 'cash' THEN amount ELSE 0 END), 0) as transfer_out
                FROM cash_transactions 
                WHERE DATE(created_at) = ?
            ''', (target_date,))
            
            result = cursor.fetchone()
            cash_in, cash_out, transfer_in, transfer_out = result
            
            # Get previous day closing balance
            cursor.execute('''
                SELECT closing_balance 
                FROM daily_cash_summary 
                WHERE date < ? 
                ORDER BY date DESC 
                LIMIT 1
            ''', (target_date,))
            
            prev_result = cursor.fetchone()
            opening_balance = prev_result[0] if prev_result else 0.0
            
            # Calculate closing balance
            closing_balance = opening_balance + cash_in - cash_out + transfer_in - transfer_out
            
            # Insert or update daily summary
            cursor.execute('''
                INSERT OR REPLACE INTO daily_cash_summary 
                (date, opening_balance, total_cash_in, total_cash_out, 
                 total_transfers_in, total_transfers_out, closing_balance, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                target_date, opening_balance, cash_in, cash_out,
                transfer_in, transfer_out, closing_balance,
                datetime.now().isoformat()
            ))
            
            self.db_manager.connection.commit()
            
        except Exception as e:
            logger.error(f"Error updating daily summary: {e}")
            self.db_manager.connection.rollback()

    def get_cash_flow_report(self, start_date: str, end_date: str) -> Dict:
        """Get cash flow report for date range"""
        try:
            cursor = self.db_manager.connection.cursor()
            
            cursor.execute('''
                SELECT 
                    DATE(created_at) as date,
                    SUM(CASE WHEN transaction_type = 'in' THEN amount ELSE 0 END) as daily_in,
                    SUM(CASE WHEN transaction_type = 'out' THEN amount ELSE 0 END) as daily_out,
                    SUM(CASE WHEN transaction_type = 'transfer' AND to_method = 'cash' THEN amount ELSE 0 END) as transfer_in,
                    SUM(CASE WHEN transaction_type = 'transfer' AND from_method = 'cash' THEN amount ELSE 0 END) as transfer_out
                FROM cash_transactions 
                WHERE DATE(created_at) BETWEEN ? AND ?
                GROUP BY DATE(created_at)
                ORDER BY date
            ''', (start_date, end_date))
            
            results = cursor.fetchall()
            
            report = {
                'dates': [],
                'cash_in': [],
                'cash_out': [],
                'transfers_in': [],
                'transfers_out': [],
                'net_flow': []
            }
            
            for row in results:
                date_str, cash_in, cash_out, transfer_in, transfer_out = row
                net = (cash_in + transfer_in) - (cash_out + transfer_out)
                
                report['dates'].append(date_str)
                report['cash_in'].append(cash_in or 0)
                report['cash_out'].append(cash_out or 0)
                report['transfers_in'].append(transfer_in or 0)
                report['transfers_out'].append(transfer_out or 0)
                report['net_flow'].append(net)
            
            return report
            
        except Exception as e:
            logger.error(f"Error getting cash flow report: {e}")
            return {}
