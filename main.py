import ollama
import subprocess
import os
MODEL = "mistral-nemo:12b"

def confirm_and_run(command: str, verbose = True) -> str:
    choice = input(f"\n[Run Command?] {command} [y/N] ").strip().lower()
    if choice != "y":
        return "User chose not to execute the command."
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    output_lines = []
    for line in process.stdout:
        output_lines.append(line)
        if verbose:
            print(line, end="", flush=True)
    process.wait()
    output = "".join(output_lines)
    return output if output else "(no output)"
    # result = subprocess.run(command,shell=True,capture_output=True,text=True)
    # output = result.stdout + result.stderr
    # return output if output else "(no output)"



messages = [{"role": "system", "content": open("agent.md", "r").read()+open("SKILL.md", "r").read()}]
while True:
    user_input = input("\nUser > ")
    messages.append({"role": "user", "content": user_input})
    while True:
        response = ollama.chat(model=MODEL, messages=messages)
        reply = response["message"]["content"]
        print(reply)
        messages.append({"role": "assistant", "content": reply})
        if reply.strip().startswith("FINISH:"):
            break
        command_result = confirm_and_run(reply.strip().split("COMMAND:")[1].strip())
        messages.append({"role": "user", "content": f"EXECUTED {command_result}"})