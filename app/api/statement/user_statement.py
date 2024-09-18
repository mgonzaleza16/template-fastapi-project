class UserStatement:
    @staticmethod
    def get_users(limit: int = None) -> str:
        if limit is not None:
            query = f"SELECT * FROM analytics.users LIMIT {limit};"
            return query
        else:
            query = "SELECT * FROM analytics.users"
            return query

    @staticmethod
    def find_by_email(email: str, limit: int = None) -> str:
        if limit is not None:
            query = f"SELECT * FROM analytics.users WHERE email = {email} LIMIT {limit};"
            return query
        else:
            query = f"SELECT * FROM analytics.users WHERE email = {email}"
            return query
