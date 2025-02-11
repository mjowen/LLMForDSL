from ollama import ChatResponse, chat

import dsl

debug = True

# Create a Genome
genome = dsl.Genome()

available_functions = {
    'addSynComp': genome.addSynComp,
    'removeSynComp': genome.removeSynComp,
    'report': genome.report,
}

def process_input(msg):
    operations = []
    messages = [{'role': 'user', 'content': msg}]

    response: ChatResponse = chat('llama3-groq-tool-use:8b', messages=messages, 
                                  tools=[genome.addSynComp, genome.removeSynComp, genome.report],
                                  options={'temperature': 0}, # Important to make results deterministic (and to have it work properly)
                                  )
    if debug:
        print(response)
    if response.message.tool_calls:
        # There may be multiple tool calls in the response
        for tool in response.message.tool_calls:
            # Ensure the function is available, and then call it
            if function_to_call := available_functions.get(tool.function.name):
                if debug:
                    print('Calling function:', tool.function.name)
                    print('Arguments:', tool.function.arguments)
                function_to_call(**tool.function.arguments)
                operations.append((tool.function.name, tool.function.arguments))
            else:
                print('Function', tool.function.name, 'not found')
    else:
        print(response.message.content)
    return operations

def generateFromOps(operations):
    genome = dsl.Genome()
    available_functions = {
        'addSynComp': genome.addSynComp,
        'removeSynComp': genome.removeSynComp,
        'report': genome.report,
    }
    for op in operations:
        for o in op:
            if o[0] == 'report':
                pass
            else:
                available_functions.get(o[0])(**o[1])
    return genome, available_functions


operations = []
while True:
    msg = input('Ready for input (natural language, undo, or exit):\n')
    if msg == 'exit':
        break
    elif msg == 'undo':
        if operations:
            operations.pop()
            genome, available_functions = generateFromOps(operations)
        else:
            print('No operations to undo')
    else:
        operations.append(process_input(msg))
    if debug:
        genome.report()
