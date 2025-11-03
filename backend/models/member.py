class Member:
    def __init__(self, member_id, name, email):
        self.member_id = member_id
        self.name = name
        self.email = email

    def create_member(self, conn):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO members (id, name, email) VALUES (?, ?, ?)", 
                       (self.member_id, self.name, self.email))
        conn.commit()

    def update_member(self, conn):
        cursor = conn.cursor()
        cursor.execute("UPDATE members SET name = ?, email = ? WHERE id = ?", 
                       (self.name, self.email, self.member_id))
        conn.commit()

    def delete_member(self, conn):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM members WHERE id = ?", (self.member_id,))
        conn.commit()