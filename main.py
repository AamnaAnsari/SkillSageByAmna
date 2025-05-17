import streamlit as st
from models.user import User
from models.session import Session
from services.payment import PaymentGateway

#  (students and one coach)
db_users = {
    "alia@student.com": User(1, "Alia", "alia@student.com", role="student"),
    "sana@student.com": User(2, "Sana", "sana@student.com", role="student"),
    "amir@student.com": User(3, "Amir", "amir@student.com", role="student"),
    "amna@coach.com": User(4, "Amna", "amna@coach.com", role="coach"),
     "anum@coach.com": User(5, "Anum", "anum@coach.com", role="coach"),
}

#  sessions
sessions = [
    Session(101, "Intro to Python", "Amna", 10),
    Session(102, "Data Science", "Anum", 15),
    Session(103, "CyberSecurity", "Amna", 30),
]

# Booking data: [(session_id, student_name)]
if 'bookings' not in st.session_state:
    st.session_state.bookings = []

# App UI
st.title("🦉 SkillSage")
st.subheader("Smarter skills in shorter time")

# Dropdown to select user
user_options = {
    f"{user.name} ({user.role})": email for email, user in db_users.items()
}
selected_user_label = st.selectbox("Select your user", list(user_options.keys()))
selected_email = user_options[selected_user_label]

if st.button("Login"):
    user = db_users.get(selected_email)
    if user:
        st.session_state.user = user
    else:
        st.error("User not found")

# After login
if 'user' in st.session_state:
    user = st.session_state.user
    st.success(f"Welcome, {user.name} ({user.role})")

    # For Students
    if user.role == "student":
        st.header("Available Sessions")
        for s in sessions:
            with st.expander(s.title):
                st.write(f"Coach: {s.coach}")
                st.write(f"Price: ${s.price}")
                if st.button(f"Book {s.title}", key=f"book_{s.session_id}_{user.name}"):
                    gateway = PaymentGateway()
                    if gateway.process_payment(user, s.price):
                        st.session_state.bookings.append((s.session_id, user.name))
                        st.success(f"Booked {s.title} successfully!")

    # For Coaches
    elif user.role == "coach":
        st.header("Your Sessions")

        # List your sessions
        your_sessions = [s for s in sessions if s.coach == user.name]
        for s in your_sessions:
            st.write(f"{s.title} - ${s.price}")

        # Add new session
        st.subheader("Add a New Session")
        title = st.text_input("Session Title", key="new_title")
        price = st.number_input("Price ($)", min_value=1, key="new_price")
        if st.button("Add Session"):
            if title.strip() == "":
                st.error("Please enter a session title.")
            else:
                new_id = max([s.session_id for s in sessions]) + 1 if sessions else 1
                new_session = Session(new_id, title, user.name, price)
                sessions.append(new_session)
                st.success(f"Session '{title}' added!")

        # Show bookings for this coach
        st.subheader("Your Bookings")
        booked_session_ids = set(b[0] for b in st.session_state.bookings)
        booked_your_sessions = [s for s in your_sessions if s.session_id in booked_session_ids]

        if booked_your_sessions:
            total_earnings = 0
            for sess in booked_your_sessions:
                booked_students = [b[1] for b in st.session_state.bookings if b[0] == sess.session_id]
                for student in booked_students:
                    st.write(f"Student: {student} booked '{sess.title}' for ${sess.price}")
                    total_earnings += sess.price
            st.write(f"**Total Earnings:** ${total_earnings}")
        else:
            st.write("No bookings yet.")
