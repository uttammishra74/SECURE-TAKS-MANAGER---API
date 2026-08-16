import streamlit as st

from api import (
    register,
    login,
    get_tasks,
    create_task,
    update_task,
    delete_task,
    delete_all_tasks,
)

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="TaskFlow",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(99, 102, 241, 0.10),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(168, 85, 247, 0.08),
                transparent 30%
            ),
            #080b12;
    }

    html, body, [class*="css"] {
        font-family: Inter, -apple-system, BlinkMacSystemFont,
        "Segoe UI", sans-serif;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    /* SIDEBAR */

    section[data-testid="stSidebar"] {
        background: #0b0f17;
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    /* BRAND */

    .brand {
        font-size: 24px;
        font-weight: 750;
        letter-spacing: -1px;
        color: #f5f7fb;
        margin-bottom: 2px;
    }

    .brand span {
        color: #818cf8;
    }

    .brand-caption {
        color: #6f7789;
        font-size: 12px;
        margin-bottom: 30px;
    }

    /* HEADERS */

    .hero-title {
        font-size: 42px;
        font-weight: 700;
        letter-spacing: -1.5px;
        color: #f4f6fb;
        margin-bottom: 5px;
    }

    .hero-subtitle {
        color: #8b93a7;
        font-size: 15px;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 20px;
        font-weight: 650;
        color: #f1f3f8;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    /* METRIC CARDS */

    .metric-card {
        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.055),
                rgba(255,255,255,0.025)
            );

        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 22px;
        min-height: 115px;

        box-shadow:
            0 10px 30px rgba(0,0,0,0.18);
    }

    .metric-label {
        color: #7f8799;
        font-size: 13px;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #f5f7fb;
        font-size: 32px;
        font-weight: 700;
    }

    /* TASK CARDS */

    .task-box {
        background: #0d121c;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 12px;
    }

    .task-title {
        font-size: 17px;
        font-weight: 650;
        color: #f2f4f8;
    }

    .task-description {
        font-size: 14px;
        color: #8b93a7;
        margin-top: 7px;
    }

    .task-meta {
        font-size: 11px;
        color: #626a7c;
        margin-top: 12px;
    }

    /* LOGIN */

    .login-container {
        max-width: 460px;
        margin: 80px auto;
    }

    .login-logo {
        font-size: 42px;
        color: #818cf8;
        margin-bottom: 15px;
    }

    .login-title {
        font-size: 38px;
        font-weight: 750;
        letter-spacing: -1.2px;
        color: #f5f7fb;
    }

    .login-subtitle {
        color: #858da0;
        margin-bottom: 30px;
    }

    /* INPUTS */

    div[data-baseweb="input"],
    div[data-baseweb="textarea"] {
        background: #0f141e !important;
        border-radius: 10px !important;
    }

    /* BUTTONS */

    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 42px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "token" not in st.session_state:
    st.session_state.token = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "email" not in st.session_state:
    st.session_state.email = ""

if "task_created" not in st.session_state:
    st.session_state.task_created = False


# ============================================================
# LOGIN / REGISTER
# ============================================================

if not st.session_state.logged_in:

    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    st.markdown('<div class="login-logo">◈</div>', unsafe_allow_html=True)

    st.markdown('<div class="login-title">Welcome back.</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="login-subtitle">'
        "Manage your tasks from one simple workspace."
        "</div>",
        unsafe_allow_html=True,
    )

    login_tab, register_tab = st.tabs(["Sign in", "Create account"])

    # --------------------------------------------------------
    # LOGIN
    # --------------------------------------------------------

    with login_tab:

        email = st.text_input(
            "Email",
            placeholder="you@example.com",
            key="login_email",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password",
        )

        if st.button(
            "Sign in",
            type="primary",
            use_container_width=True,
        ):

            if not email or not password:

                st.warning("Please enter your email and password.")

            else:

                try:

                    response = login(email, password)

                    if response.status_code == 200:

                        data = response.json()

                        st.session_state.token = data["access_token"]

                        st.session_state.logged_in = True

                        st.session_state.email = email

                        st.rerun()

                    else:

                        try:
                            error = response.json().get(
                                "detail", "Invalid email or password."
                            )
                        except:
                            error = "Invalid email or password."

                        st.error(error)

                except Exception as e:

                    st.error(f"Unable to connect to API: {e}")

    # --------------------------------------------------------
    # REGISTER
    # --------------------------------------------------------

    with register_tab:

        name = st.text_input(
            "Full name",
            placeholder="Your name",
            key="register_name",
        )

        email = st.text_input(
            "Email",
            placeholder="you@example.com",
            key="register_email",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password",
            key="register_password",
        )

        if st.button(
            "Create account",
            use_container_width=True,
        ):

            if not name or not email or not password:

                st.warning("Please complete all fields.")

            else:

                try:

                    response = register(
                        name,
                        email,
                        password,
                    )

                    if response.status_code in [200, 201]:

                        st.success("Account created successfully.")

                        st.info("You can now sign in.")

                    else:

                        try:
                            error = response.json().get(
                                "detail", "Registration failed."
                            )
                        except:
                            error = "Registration failed."

                        st.error(error)

                except Exception as e:

                    st.error(f"Unable to connect to API: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="brand">Task<span>Flow</span></div>', unsafe_allow_html=True
    )

    st.markdown(
        '<div class="brand-caption">' "Secure task management" "</div>",
        unsafe_allow_html=True,
    )

    st.caption("WORKSPACE")

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Create task",
            "Update task",
            "Delete task",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.caption("ACCOUNT")

    st.write(st.session_state.email)

    if st.button(
        "Sign out",
        use_container_width=True,
    ):

        st.session_state.token = None
        st.session_state.logged_in = False
        st.session_state.email = ""

        st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.markdown('<div class="hero-title">Dashboard</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="hero-subtitle">'
        "A clear overview of your current workload."
        "</div>",
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # LOAD TASKS
    # --------------------------------------------------------

    try:

        response = get_tasks()

    except Exception as e:

        st.error(f"Unable to connect to FastAPI: {e}")

        st.stop()

    if response.status_code == 200:

        tasks = response.json()

        total = len(tasks)

        completed = sum(1 for task in tasks if task["completed"])

        pending = total - completed

        completion_rate = round(completed / total * 100) if total > 0 else 0

        # ----------------------------------------------------
        # METRICS
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">
                        Total tasks
                    </div>
                    <div class="metric-value">
                        {total}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">
                        Completed
                    </div>
                    <div class="metric-value">
                        {completed}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col3:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">
                        Pending
                    </div>
                    <div class="metric-value">
                        {pending}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col4:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">
                        Completion
                    </div>
                    <div class="metric-value">
                        {completion_rate}%
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # ----------------------------------------------------
        # TASKS
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">Your tasks</div>', unsafe_allow_html=True
        )

        if not tasks:

            st.info("You don't have any tasks yet.")

        else:

            for task in tasks:

                # IMPORTANT:
                # We are NOT putting task text inside
                # custom HTML anymore.

                with st.container(border=True):

                    top_col, status_col = st.columns([5, 1])

                    with top_col:

                        st.markdown(f"### {task['title']}")

                    with status_col:

                        if task["completed"]:

                            st.success("Completed")

                        else:

                            st.warning("Pending")

                    if task["description"]:

                        st.write(task["description"])

                    else:

                        st.caption("No description provided.")

                    st.caption(f"Task ID: #{task['id']}")

    else:

        st.error(f"Unable to load tasks. " f"API returned {response.status_code}.")


# ============================================================
# CREATE TASK
# ============================================================

elif page == "Create task":

    st.markdown('<div class="hero-title">Create task</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="hero-subtitle">' "Add something new to your workspace." "</div>",
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # SUCCESS MESSAGE FROM PREVIOUS CREATE
    # --------------------------------------------------------

    if st.session_state.task_created:

        st.success("Task created successfully.")

        st.session_state.task_created = False

    # --------------------------------------------------------
    # FORM
    # --------------------------------------------------------

    with st.container(border=True):

        title = st.text_input(
            "Task title",
            placeholder="e.g. Complete API documentation",
        )

        description = st.text_area(
            "Description",
            placeholder="Describe what needs to be done...",
        )

        completed = st.checkbox("Mark as completed")

        st.write("")

        if st.button(
            "Create task",
            type="primary",
        ):

            if not title.strip():

                st.warning("Please enter a task title.")

            else:

                try:

                    response = create_task(
                        title.strip(),
                        description.strip(),
                        completed,
                        st.session_state.token,
                    )

                    if response.status_code in [200, 201]:

                        st.session_state.task_created = True

                        st.success("Task saved successfully.")

                        st.write("Your task has been added to the database.")

                        # Show exactly what the API returned

                        try:

                            created_task = response.json()

                            st.caption(f"Task ID: #{created_task['id']}")

                        except:

                            pass

                    else:

                        try:

                            error = response.json().get(
                                "detail", "Unable to create task."
                            )

                        except:

                            error = "Unable to create task."

                        st.error(error)

                except Exception as e:

                    st.error(f"API connection error: {e}")


# ============================================================
# UPDATE TASK
# ============================================================

elif page == "Update task":

    st.markdown('<div class="hero-title">Update task</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="hero-subtitle">' "Modify an existing task." "</div>",
        unsafe_allow_html=True,
    )

    with st.container(border=True):

        task_id = st.number_input(
            "Task ID",
            min_value=1,
            step=1,
        )

        title = st.text_input("New title")

        description = st.text_area("New description")

        completed = st.checkbox("Completed")

        if st.button(
            "Save changes",
            type="primary",
        ):

            try:

                response = update_task(
                    task_id,
                    title,
                    description,
                    completed,
                )

                if response.status_code == 200:

                    st.success("Task updated successfully.")

                    st.json(response.json())

                else:

                    try:

                        error = response.json().get("detail", "Task not found.")

                    except:

                        error = "Task not found."

                    st.error(error)

            except Exception as e:

                st.error(f"API connection error: {e}")


# ============================================================
# DELETE TASK
# ============================================================

elif page == "Delete task":

    st.markdown('<div class="hero-title">Delete task</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="hero-subtitle">' "Remove tasks from your workspace." "</div>",
        unsafe_allow_html=True,
    )

    tab1, tab2 = st.tabs(
        [
            "Delete task",
            "Delete everything",
        ]
    )

    # --------------------------------------------------------
    # DELETE ONE
    # --------------------------------------------------------

    with tab1:

        with st.container(border=True):

            task_id = st.number_input(
                "Task ID",
                min_value=1,
                step=1,
            )

            if st.button(
                "Delete task",
                type="primary",
            ):

                try:

                    response = delete_task(task_id)

                    if response.status_code == 200:

                        st.success("Task deleted successfully.")

                    else:

                        try:

                            error = response.json().get("detail", "Task not found.")

                        except:

                            error = "Task not found."

                        st.error(error)

                except Exception as e:

                    st.error(f"API connection error: {e}")

    # --------------------------------------------------------
    # DELETE ALL
    # --------------------------------------------------------

    with tab2:

        with st.container(border=True):

            st.warning("This will permanently delete every task.")

            confirm = st.checkbox("I understand this action cannot be undone.")

            if st.button(
                "Delete all tasks",
                type="primary",
            ):

                if not confirm:

                    st.warning("Please confirm before continuing.")

                else:

                    try:

                        response = delete_all_tasks()

                        if response.status_code in [
                            200,
                            204,
                        ]:

                            st.success("All tasks have been deleted.")

                        else:

                            try:

                                error = response.json().get(
                                    "detail", "Unable to delete tasks."
                                )

                            except:

                                error = "Unable to delete tasks."

                            st.error(error)

                    except Exception as e:

                        st.error(f"API connection error: {e}")
