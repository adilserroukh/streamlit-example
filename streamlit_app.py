import os
import streamlit as st
import subprocess
from streamlit_monaco import st_monaco
from diagrams import Diagram

DIAGRAM_INSTRUCTIONS = """
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

with Diagram("Grouped Workers", show=False, direction="TB"):
    ELB("lb") >> [EC2("worker1"),
                  EC2("worker2"),
                  EC2("worker3"),
                  EC2("worker4"),
                  EC2("worker5")] >> RDS("events")
"""

st.header("Chat Window")
content = st_monaco(
    value=DIAGRAM_INSTRUCTIONS,
    height="200px",
    language="python",
    lineNumbers=True,
    minimap=False,
    theme="vs-dark",
)

if st.button("Generate Diagram"):
    # Delete image if exists
    try:
        os.remove("grouped_workers.png")
    except FileNotFoundError:
        print(f"File grouped_workers.png not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    with st.spinner("Generating ..."):
        process = subprocess.run(['python', "-c", content], capture_output=True)
        if process.returncode == 0:
            st.image('grouped_workers.png')
            # Dowlnoad the file
            with open("grouped_workers.png", "rb") as file:
                btn = st.download_button(
                    label="Download Diagram",
                    data=file,
                    file_name="grouped_workers.png",
                    mime="image/png"
                )
        else:
            st.write(process.stderr.decode("utf-8"))
