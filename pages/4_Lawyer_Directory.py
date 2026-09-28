import streamlit as st

st.set_page_config(
    page_title="Find a Lawyer | LawVista",
    page_icon="👨‍⚖️",
    layout="wide"
)

st.title("👨‍⚖️ Find a Lawyer")
st.write(
    "Search lawyers by city and area of practice and access "
    "public professional contact sources."
)

# Search
search = st.text_input(
    "🔎 Search Lawyer",
    placeholder="Enter lawyer name, city, specialization or bar..."
)

col1, col2 = st.columns(2)

with col1:
    city = st.selectbox(
        "City / Region",
        [
            "All Pakistan",
            "Islamabad",
            "Rawalpindi",
            "Lahore",
            "Karachi",
            "Peshawar",
            "Quetta",
            "Muzaffarabad",
            "Mirpur",
            "Gilgit"
        ]
    )

with col2:
    specialization = st.selectbox(
        "Area of Practice",
        [
            "All Areas",
            "Criminal Law",
            "Civil Law",
            "Family Law",
            "Constitutional Law",
            "Corporate Law",
            "Cyber Crime",
            "Tax Law",
            "Property Law",
            "Labour Law",
            "Banking Law"
        ]
    )

st.divider()
lawyers = [
    {
        "name": "Advocate Ayesha Khan",
        "city": "Islamabad",
        "specialization": "Constitutional Law",
        "experience": "10 Years",
        "bar": "Islamabad Bar Association",
        "status": "Verified"
    },
    {
        "name": "Advocate Ali Raza",
        "city": "Lahore",
        "specialization": "Criminal Law",
        "experience": "8 Years",
        "bar": "Lahore Bar Association",
        "status": "Verified"
    },
    {
        "name": "Advocate Sara Ahmed",
        "city": "Karachi",
        "specialization": "Corporate Law",
        "experience": "12 Years",
        "bar": "Karachi Bar Association",
        "status": "Verified"
    },
    {
        "name": "Advocate Hamza Khan",
        "city": "Peshawar",
        "specialization": "Civil Law",
        "experience": "7 Years",
        "bar": "Peshawar Bar Association",
        "status": "Verified"
    },
    {
        "name": "Advocate Fatima Baloch",
        "city": "Quetta",
        "specialization": "Family Law",
        "experience": "9 Years",
        "bar": "Balochistan Bar Council",
        "status": "Verified"
    }
]

filtered_lawyers = []
for lawyer in lawyers:
    matches_search = (
        not search
        or search.lower() in lawyer["name"].lower()
        or search.lower() in lawyer["city"].lower()
        or search.lower() in lawyer["specialization"].lower()
    )

    matches_city = (
        city == "All Pakistan"
        or lawyer["city"] == city
    )

    matches_specialization = (
        specialization == "All Areas"
        or lawyer["specialization"] == specialization
    )

    if matches_search and matches_city and matches_specialization:
        filtered_lawyers.append(lawyer)
st.subheader("📋 Lawyer Directory")

if filtered_lawyers:
    st.success(f"Found {len(filtered_lawyers)} lawyer(s).")

    for lawyer in filtered_lawyers:
        with st.container(border=True):
            st.subheader(f"⚖️ {lawyer['name']}")
            st.write(f"**City:** {lawyer['city']}")
            st.write(f"**Specialization:** {lawyer['specialization']}")
            st.write(f"**Experience:** {lawyer['experience']}")
            st.write(f"**Bar / Association:** {lawyer['bar']}")
            st.write(f"**Verification:** {lawyer['status']}")
else:
    st.warning("No lawyers found matching your search and filters.")

st.divider()

st.subheader("👤 Lawyer Profile")

col1, col2 = st.columns(2)

with col1:
    st.write("**Name:** —")
    st.write("**Specialization:** —")
    st.write("**Experience:** —")
    st.write("**City:** —")

with col2:
    st.write("**Bar / Association:** —")
    st.write("**Enrollment / Verification:** —")
    st.write("**Professional Contact:** —")
    st.write("**Office Information:** —")

st.subheader("🔗 Contact & Verification Sources")

st.write(
    """
    LawVista can provide links to publicly available professional
    contact and verification sources, such as:

    • Pakistan Bar Council  
    • Provincial Bar Councils  
    • Islamabad Bar Council  
    • Recognized Bar Associations  
    • Public law-firm / professional profiles  
    • Other verified public professional sources
    """
)

st.warning(
    "LawVista should display only public professional contact information. "
    "Users should independently verify a lawyer's enrollment and credentials "
    "before engaging professional services."
)