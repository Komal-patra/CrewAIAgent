import os

file_path = r"C:/Komal_notes/LLM_RAG_Personal_projects/AI_Agents/CrewAIAgent/PDF_RAG_CrewAI/pdf_rag_crewai/src/example_home_inspection.pdf"
if os.path.exists(file_path):
    print("File found!")
else:
    print("File not found.")
