import logging
from crewai import Agent, Crew, Process, Task
from crewai_tools import PDFSearchTool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging to track the flow of the process
logging.basicConfig(level=logging.DEBUG)

#------------------Tools------------------#

# Initialize PDF Search Tool with absolute file path
pdf_search_tool = PDFSearchTool(
    pdf=r"C:/Komal_notes/LLM_RAG_Personal_projects/AI_Agents/CrewAIAgent/PDF_RAG_CrewAI/pdf_rag_crewai/src/example_home_inspection.pdf",
)

#-----------------Agents-------------------#

# Research Agent: searches through the PDF for relevant answers
research_agent = Agent(
    role="Research Agent",
    goal="search through the PDF to find the relevant answers",
    allow_delegation=False,
    verbose=True,  # This will print detailed logs from the agent
    backstory=(
        """
        The research agent is adept at searching and 
        extracting data from documents, ensuring accurate and prompt responses.
        """
    ),
    tools=[pdf_search_tool],
)

# Professional Writer Agent: writes professional emails based on the research agent's findings
professional_writer_agent = Agent(
    role="Professional Writer",
    goal="Write professional emails based on the research agent's findings",
    allow_delegation=False,
    verbose=True,  # This will print detailed logs from the agent
    backstory=(
        """
        The professional writer agent has excellent writing skills and is able to craft 
        clear and concise emails based on the provided information.
        """
    ),
    tools=[],  # No additional tools required for this agent
)

#-------------------Tasks-----------------#

# Task 1: Research Agent searches the PDF to answer the customer's question
answer_customer_question_task = Task(
    description=(
        """
        Answer the customer's questions based on the home inspection PDF.
        The research agent will search through the PDF to find the relevant answers.
        Your final answer MUST be clear and accurate, based on the content of the home
        inspection PDF.

        Here is the customer's question:
        {customer_question}
        """
    ),
    expected_output="""
        Provide clear and accurate answers to the customer's questions based on 
        the content of the home inspection PDF.
        """,
    tools=[pdf_search_tool],
    agent=research_agent,
)

# Task 2: Professional Writer Agent writes an email to a contractor
write_email_task = Task(
    description=(
        """
        - Write a professional email to a contractor based 
            on the research agent's findings.
        - The email should clearly state the issues found in the specified section 
            of the report and request a quote or action plan for fixing these issues.
        - Ensure the email is signed with the following details:
        
            Best regards,

            Brandon Hancock,
            Hancock Realty
        """
    ),
    expected_output="""
        Write a clear and concise email that can be sent to a contractor to address the 
        issues found in the home inspection report.
        """,
    tools=[],  # No tools needed for the writing agent
    agent=professional_writer_agent,
)

#--------------------CREW-----------------#

# Crew configuration: execute tasks sequentially
crew = Crew(
    agents=[research_agent, professional_writer_agent],
    tasks=[answer_customer_question_task, write_email_task],
    process=Process.sequential,  # Ensure tasks are executed one after the other
)

# Get customer's question input
customer_question = input("Which section of the report would you like to generate a work order for?\n")

# Debugging: print input
logging.debug(f"Customer question: {customer_question}")

# Execute the crew process and handle any errors
try:
    # Kickoff the crew process with the provided customer question
    result = crew.kickoff(inputs={"customer_question": customer_question})
    
    # Log the result
    logging.debug("Crew kickoff result:")
    print(result)
    
except Exception as e:
    # Catch and print any errors during the process execution
    logging.error(f"An error occurred during the crew process: {e}")
    print(f"An error occurred: {e}")

