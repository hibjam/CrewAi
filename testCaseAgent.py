import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

os.environ["OPENAI_API_KEY"] = ""

api = os.environ.get("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"]="gpt-3.5-turbo"


productManager = Agent(
    role = "Product Manager", 
    goal = "You are the professional responsible for the development and execution of a product vision", 
    backstory = """You are the bridge between various teams involved in the product development process, such as engineering, design, marketing, and sales. You 
                     articulate the vision and goals for the product, considering market trends, customer needs, and business objectives whilst at the same time 
                     gather feedback from customers, stakeholders, and internal teams to prioritize features and improvements.""",
    verbose = True, 
    allow_delegation = False
)

businessAnalyst = Agent(
    role = "Business Analyst", 
    goal = "Understand the system under test and determine requirements for what this system should be able to do",
    backstory = """You play a crucial role in the tech industry by bridging the gap between business needs and technology solutions. Your job is to gather requirements, 
                working closely with stakeholders, including clients, users, and project teams, to understand business objectives and document requirements. You then 
                analyze these gathered requirements to ensure they are clear, complete, and feasible. You facilitate communication, clarify requirements, 
                and manage expectations to ensure that everyone is aligned on project goals and deliverables.
                """,
    verbose = True, 
    allow_delegation = True
)

tester = Agent(
    role = "Quality Assurance Engineer", 
    goal = "Ensuring the quality, reliability, and performance of software applications", 
    backstory = """You also collaborate with stakeholders to understand project requirements and define test objectives, scope, and strategies. 
                They create test plans outlining the testing approach, test scenarios, and test cases to be executed. You design test cases based 
                on functional and non-functional requirements, user stories, and acceptance criteria. You identify test scenarios, determine test data, 
                and develop test scripts or procedures to verify the functionality and behavior of the software. You are not a performance engineer.
                """, 
    verbose = True, 
)

task1 = Task (
    description = """You have started work on the website for a new up and coming bank. You need to start thinking of the homepage for this website. This begins with defining the product vision:
                    understanding the target audience which will be new customers and defining the primary goals of the homepage (e.g., to provide account access, promote new products, 
                    improve customer engagement). You collaberate with stakeholders to gather requirements and conduct market research and analyze competitor websites to identify best practices.""",
    expected_output = "Detialed requirements of what we need from the homepage",               
    agent = productManager
)

task2 = Task(
    description = """Analyse what the requirements are for the homepage that have been given to you by the product managerand from that generate some acceptance criteria that the homepage 
                    must meet to be accepted by the stakeholders, typically the product owner or the customer. These criteria should be specifc, measureable, 
                    testable, complete, aligned with user needs and be achievable within a specific time frame""", 
    expected_output = "Detialed acceptance critera in Given, When, Then format",               
    agent = businessAnalyst
)

task3 = Task (
    description = """Based on the acceptance criteria created by the business analyst, create detailed test cases for how these criteria are going to be met, this should ensure that 
                    the test case is able to Identify the Test Objective, Define Pre-Conditions, Define the test steps, specify any input data, Expected results, test execution instrcutions,
                    post conditions, any cleanup steps and any extra additional infomration you think might be useful. Examples of this includes things like making sure each link works on a webpage, 
                    testing form validation and testing authentication as well as content of the page.""",
    expected_output = "Full set of test cases based on the acceptance criteria",
    agent = tester                
)

crew = Crew(
  agents=[productManager, businessAnalyst, tester],
  tasks=[task1, task2, task3],
  verbose=2, # You can set it to 1 or 2 to different logging levels
)


result = crew.kickoff()

print("######################")
print(result)
