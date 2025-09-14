"""Email service."""

import logging
from typing import Optional
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Email service for sending notifications."""
    
    def __init__(self):
        self.sendgrid_client = None
        if settings.sendgrid_api_key:
            self.sendgrid_client = SendGridAPIClient(api_key=settings.sendgrid_api_key)
    
    async def send_magic_link(self, email: str, token: str) -> bool:
        """Send magic link email."""
        magic_link = f"{settings.app_base_url}/auth/callback?token={token}"
        
        if self.sendgrid_client:
            try:
                message = Mail(
                    from_email=settings.alerts_from_email,
                    to_emails=email,
                    subject="Your Habit Loop Login Link",
                    html_content=f"""
                    <h2>Welcome to Habit Loop!</h2>
                    <p>Click the link below to log in:</p>
                    <a href="{magic_link}" style="background-color: #4F46E5; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">Login to Habit Loop</a>
                    <p>This link will expire in 15 minutes.</p>
                    <p>If you didn't request this, please ignore this email.</p>
                    """
                )
                response = self.sendgrid_client.send(message)
                logger.info(f"Magic link sent to {email}, status: {response.status_code}")
                return response.status_code < 400
            except Exception as e:
                logger.error(f"Failed to send magic link to {email}: {e}")
                return False
        else:
            # Development fallback
            logger.info(f"DEV: Magic link for {email}: {magic_link}")
            return True
    
    async def send_reminder(self, email: str, habit_title: str, checkin_url: str) -> bool:
        """Send habit reminder email."""
        if self.sendgrid_client:
            try:
                message = Mail(
                    from_email=settings.alerts_from_email,
                    to_emails=email,
                    subject=f"Reminder: {habit_title}",
                    html_content=f"""
                    <h2>Time for your habit: {habit_title}</h2>
                    <p>Don't break your streak! Click below to check in:</p>
                    <a href="{checkin_url}" style="background-color: #10B981; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">Check In</a>
                    <p>Or <a href="{checkin_url}&action=snooze">snooze for later</a></p>
                    """
                )
                response = self.sendgrid_client.send(message)
                logger.info(f"Reminder sent to {email} for {habit_title}, status: {response.status_code}")
                return response.status_code < 400
            except Exception as e:
                logger.error(f"Failed to send reminder to {email}: {e}")
                return False
        else:
            # Development fallback
            logger.info(f"DEV: Reminder for {email} - {habit_title}: {checkin_url}")
            return True
    
    async def send_weekly_digest(self, email: str, insights: dict) -> bool:
        """Send weekly digest email."""
        if self.sendgrid_client:
            try:
                message = Mail(
                    from_email=settings.alerts_from_email,
                    to_emails=email,
                    subject="Your Weekly Habit Loop Report",
                    html_content=f"""
                    <h2>Your Weekly Habit Report</h2>
                    <p>Completion Rate: {insights.get('completion_rate', 0):.1%}</p>
                    <p>Streak Health Score: {insights.get('streak_health_score', 0)}/100</p>
                    <p>Keep up the great work!</p>
                    """
                )
                response = self.sendgrid_client.send(message)
                logger.info(f"Weekly digest sent to {email}, status: {response.status_code}")
                return response.status_code < 400
            except Exception as e:
                logger.error(f"Failed to send weekly digest to {email}: {e}")
                return False
        else:
            # Development fallback
            logger.info(f"DEV: Weekly digest for {email}: {insights}")
            return True


email_service = EmailService()
