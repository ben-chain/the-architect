import os
import json
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from helpers import load_phase_file, get_run_num, write_phase_output, get_phase_output, copy_prev_phase_outputs, get_phase_num, update_prev_phase_outputs

load_dotenv()

chat = ChatOpenAI(temperature=0.8,model_name='gpt-4')
system_template = ""
with open('system_template.txt', 'r') as file:
    system_template = file.read()

system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

def run_vision_phase(prev_phase_outputs):
    prompt = load_phase_file(get_phase_num('vision', phases))
    human_message_prompt = HumanMessagePromptTemplate.from_template(prompt)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    project = prev_phase_outputs["project"]
    vision_result = chat(chat_prompt.format_prompt(project=project).to_messages())
    vision_output_full = vision_result.content

    print('ran vision phase:')
    print(vision_output_full)

    # Find the indices of the section headers
    feature_index = vision_output_full.find("## MVP Features")
    overview_index = vision_output_full.find("## Project MVP Overview")

    # Extract the sections
    mvp_features = vision_output_full[feature_index:overview_index].strip()
    project_overview = vision_output_full[overview_index:].strip()

    vision_output_structured = {
        'overview': project_overview,
        'features': mvp_features
    }

    return vision_output_full, vision_output_structured

def run_inputs_phase(prev_phase_outputs):
    prompt = load_phase_file(get_phase_num('inputs', phases))
    human_message_prompt = HumanMessagePromptTemplate.from_template(prompt)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    project = prev_phase_outputs["project"]
    overview = prev_phase_outputs["vision"]["overview"]
    features = prev_phase_outputs["vision"]["features"]

    inputs_result = chat(chat_prompt.format_prompt(project=project, overview=overview, features=features).to_messages())
    inputs_output_full = inputs_result.content

    print('ran inputs phase:')
    print(inputs_output_full)

    final_state_index = inputs_output_full.find("# Fundamental Program Inputs")
    fundamental_inputs = inputs_output_full[final_state_index:].strip()
    inputs_output_structured = {
        'fundamental_inputs': fundamental_inputs
    }

    return inputs_output_full, inputs_output_structured

def run_states_phase(prev_phase_outputs):
    prompt = load_phase_file(get_phase_num('states', phases))
    human_message_prompt = HumanMessagePromptTemplate.from_template(prompt)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    # project = prev_phase_outputs["project"]
    # vision_context = prev_phase_outputs["vision"]["overview"] + "\n" + prev_phase_outputs["vision"]["features"]
    project = prev_phase_outputs["project"]
    overview = prev_phase_outputs["vision"]["overview"]
    features = prev_phase_outputs["vision"]["features"]
    fundamental_inputs = prev_phase_outputs["inputs"]["fundamental_inputs"]

    state_result = chat(chat_prompt.format_prompt(project=project, overview=overview, features=features, fundamental_inputs=fundamental_inputs).to_messages())
    state_output_full = state_result.content

    print('ran state_output phase:')
    print(state_output_full)

    final_state_index = state_output_full.find("# Fundamental State")
    fundamental_state = state_output_full[final_state_index:].strip()
    state_output_structured = {
        'fundamental_state': fundamental_state
    }

    return state_output_full, state_output_structured

def run_machine_phase(prev_phase_outputs):
    prompt = load_phase_file(get_phase_num('machine', phases))
    human_message_prompt = HumanMessagePromptTemplate.from_template(prompt)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    project = prev_phase_outputs["project"]
    overview = prev_phase_outputs["vision"]["overview"]
    features = prev_phase_outputs["vision"]["features"]
    state = prev_phase_outputs["states"]["fundamental_state"]

    machine_result = chat(chat_prompt.format_prompt(project=project, overview=overview, features=features, state=state).to_messages())
    machine_output_full = machine_result.content

    print('ran machinist phase:')
    print(machine_output_full)

    machine_output_structured = {
        'machine': machine_output_full
    }

    return machine_output_full, machine_output_structured

prev_phase_outputs = {
    'project': "An emoji-themed chess game written in javascript to run locally in the browser between two players"
}

phases = {
    1: ('vision', run_vision_phase),
    2: ('inputs', run_inputs_phase),
    3: ('states', run_states_phase)
    # 3: ('machine', run_machine_phase)
}

project = "An emoji-themed chess game written in javascript to run locally in the browser between two players"

def run_phase(run_num, phase_num):
    phase_name, phase_func = phases[phase_num]

    phase_output_full, phase_output_structured = phase_func(prev_phase_outputs)
    prev_phase_outputs[phase_name] = phase_output_structured

    write_phase_output(phase_output_full, phase_output_structured, phase_num, run_num)


run_num = get_run_num()
print("beginning run:")
print(run_num)


# Use this to resume previously completed runs
# resume_run=14
# resume_from_phase=1
# copy_prev_phase_outputs(resume_from_phase,resume_run,run_num)
# prev_phase_outputs = update_prev_phase_outputs(resume_from_phase, prev_phase_outputs, run_num, phases)

# comment out the phase running if using above to resume runs
run_phase(run_num, 1)
run_phase(run_num, 2)
run_phase(run_num, 3)