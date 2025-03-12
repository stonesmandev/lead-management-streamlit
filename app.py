import streamlit as st
import json
import pandas as pd
import io

# --- Streamlit Python Code ---

# Initialize session state
if 'leads' not in st.session_state:
    st.session_state.leads =

# Function to download CSV
def download_csv():
    """Downloads the leads as a CSV file."""
    if not st.session_state.leads:
        st.warning("No leads to download.")
        return

    df = pd.DataFrame(st.session_state.leads)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()

    st.download_button(
        label="Download Leads CSV",
        data=csv_data.encode('utf-8'),
        file_name="leads.csv",
        mime="text/csv",
    )

# HTML, CSS, and JavaScript
html_code = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width:device-width, initial-scale=1.0">
    <title>Lead Management</title>
    <style>
        /* CSS Reset */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', Arial, sans-serif;
            background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
            min-height: 100vh;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .glass-container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            padding: 30px;
            width: 90%;
            max-width: 600px;
        }

        h1 {
            color: #333;
            font-size: 2rem;
            margin-bottom: 20px;
        }

        form input,
        form textarea {
            margin: 10px 0;
            padding: 12px;
            width: calc(100% - 24px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(5px);
            font-size: 1rem;
            color: #333;
        }

        form input::placeholder,
        form textarea::placeholder {
            color: #666;
        }

        form button {
            margin: 10px 0;
            padding: 12px 24px;
            background: rgba(0, 123, 255, 0.8);
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 1rem;
            transition: background 0.3s ease;
        }

        form button:hover {
            background: rgba(0, 123, 255, 1);
        }

        table {
            width: 100%;
            margin: 20px 0;
            border-collapse: collapse;
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(5px);
            border-radius: 10px;
            overflow: hidden;
        }

        th,
        td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        th {
            background: rgba(0, 123, 255, 0.8);
            color: white;
        }

        tr:hover {
            background: rgba(255, 255, 255, 0.3);
        }
    </style>
</head>

<body>
    <div class="glass-container">
        <h1>Lead Management</h1>
        <form id="leadForm">
            <input type="text" id="name" placeholder="Name" required><br><br>
            <input type="email" id="email" placeholder="Email" required><br><br>
            <input type="tel" id="phone" placeholder="Phone" required><br><br>
            <textarea id="notes" placeholder="Notes"></textarea><br><br>
            <button type="submit">Add Lead</button>
        </form>

        <table id="leadsTable">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Notes</th>
                </tr>
            </thead>
            <tbody>
            </tbody>
        </table>
    </div>

    <script>
        const leadForm = document.getElementById('leadForm');
        const leadsTable = document.getElementById('leadsTable').querySelector('tbody');

        // Function to render the table
        function renderLeads(leads) {
            leadsTable.innerHTML = ''; // Clear existing rows

            leads.forEach(lead => {
                let row = document.createElement('tr');

                let nameCell = document.createElement('td');
                nameCell.textContent = lead.name;
                row.appendChild(nameCell);

                let emailCell = document.createElement('td');
                emailCell.textContent = lead.email;
                row.appendChild(emailCell);

                let phoneCell = document.createElement('td');
                phoneCell.textContent = lead.phone;
                row.appendChild(phoneCell);

                let notesCell = document.createElement('td');
                notesCell.textContent = lead.notes;
                row.appendChild(notesCell);

                leadsTable.appendChild(row);
            });
        }

        // Initial render (if data is available)
        if (window.streamlit && window.streamlit.setFrameHeight) {
            window.streamlit.setFrameHeight(document.documentElement.scrollHeight);
        }

        // Handle form submission
        leadForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const phone = document.getElementById('phone').value;
            const notes = document.getElementById('notes').value;

            const newLead = {
                name: name,
                email: email,
                phone: phone,
                notes: notes
            };

            // Send message to Streamlit
            if (window.streamlit && window.streamlit.setFrameHeight) {
                window.streamlit.setFrameHeight(document.documentElement.scrollHeight);
            }
            if (window.streamlit) {
                window.streamlit.setFrameHeight(document.documentElement.scrollHeight);
                window.streamlit.setComponentValue(JSON.stringify({ 'type': 'add_lead', 'lead': newLead }));
            }
            leadForm.reset();
        });

        // Listen for messages from Streamlit
        if (window.streamlit) {
            window.streamlit.onMessage(function(message) {
                if (message && message.type === 'render_leads') {
                    renderLeads(message.leads);
                }
            });
        }
    </script>
</body>

</html>
"""

# Embed the HTML in Streamlit
st.components.v1.html(html_code, height=600)  # Adjust height as needed

# Handle messages from HTML
component_value = st.session_state.get("streamlit:component_value", None)
if component_value:
    try:
        data = json.loads(component_value)
        if data['type'] == 'add_lead':
            st.session_state.leads.append(data['lead'])
            # Send updated leads back to HTML
            st.components.v1.html(f"""
                <script>
                    if (window.streamlit) {
                        window.streamlit.setFrameHeight(document.documentElement.scrollHeight);
                        window.streamlit.setComponentValue(JSON.stringify({{'type': 'render_leads', 'leads': {json.dumps(st.session_state.leads)}}}));
                    }
                </script>
            """, height=0)  # Height 0 to hide this script
    except json.JSONDecodeError:
        st.error("Invalid data format received from component.")

# Initial render of leads to HTML
st.components.v1.html(f"""
    <script>
        if (window.streamlit) {
            window.streamlit.setFrameHeight(document.documentElement.scrollHeight);
            window.streamlit.setComponentValue(JSON.stringify({{'type': 'render_leads', 'leads': {json.dumps(st.session_state.leads)}}}));
        }
    </script>
""", height=0)

# Download CSV button
download_csv()
