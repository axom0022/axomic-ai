import sys
import os
from axomicai import axomicai

def printhelp():
    print("Commands:")
    print("  trainfile <path> [epochs] [batch] [lr]")
    print("  trainurl <url> [epochs] [batch] [lr]")
    print("  trainfilestream <path> [epochs] [batch] [lr] [chunksize]")
    print("  trainurlstream <url> [epochs] [batch] [lr] [chunksize]")
    print("  export <path>")
    print("  import <path>")
    print("  undo")
    print("  redo")
    print("  chat <prompt>")
    print("  status")
    print("  exit")

def main():
    ai = axomicai()
    if os.path.exists('axomic_weights.pt'):
        ai.loadmodel('axomic_weights.pt')
        print("Loaded existing weights.")
    else:
        print("No weights found. Start training.")
    print("Axomic Ai Manager. Type 'help' for commands.")
    while True:
        cmd = input("> ").strip().split()
        if not cmd:
            continue
        if cmd[0] == "help":
            printhelp()
        elif cmd[0] == "trainfile":
            if len(cmd) < 2:
                print("Usage: trainfile <path> [epochs] [batch] [lr]")
                continue
            epochs = int(cmd[2]) if len(cmd)>2 else 1
            batch = int(cmd[3]) if len(cmd)>3 else 4
            lr = float(cmd[4]) if len(cmd)>4 else 1e-3
            ai.trainfromfile(cmd[1], epochs, batch, lr)
        elif cmd[0] == "trainurl":
            if len(cmd) < 2:
                print("Usage: trainurl <url> [epochs] [batch] [lr]")
                continue
            epochs = int(cmd[2]) if len(cmd)>2 else 1
            batch = int(cmd[3]) if len(cmd)>3 else 4
            lr = float(cmd[4]) if len(cmd)>4 else 1e-3
            ai.trainfromurl(cmd[1], epochs, batch, lr)
        elif cmd[0] == "trainfilestream":
            if len(cmd) < 2:
                print("Usage: trainfilestream <path> [epochs] [batch] [lr] [chunksize]")
                continue
            epochs = int(cmd[2]) if len(cmd)>2 else 1
            batch = int(cmd[3]) if len(cmd)>3 else 4
            lr = float(cmd[4]) if len(cmd)>4 else 1e-3
            chunksize = int(cmd[5]) if len(cmd)>5 else 200
            ai.trainfromfilestream(cmd[1], epochs, batch, lr, chunksize)
        elif cmd[0] == "trainurlstream":
            if len(cmd) < 2:
                print("Usage: trainurlstream <url> [epochs] [batch] [lr] [chunksize]")
                continue
            epochs = int(cmd[2]) if len(cmd)>2 else 1
            batch = int(cmd[3]) if len(cmd)>3 else 4
            lr = float(cmd[4]) if len(cmd)>4 else 1e-3
            chunksize = int(cmd[5]) if len(cmd)>5 else 200
            ai.trainfromurlstream(cmd[1], epochs, batch, lr, chunksize)
        elif cmd[0] == "export":
            if len(cmd) < 2:
                print("Usage: export <path>")
                continue
            ai.exportmodel(cmd[1])
            print(f"Exported to {cmd[1]}")
        elif cmd[0] == "import":
            if len(cmd) < 2:
                print("Usage: import <path>")
                continue
            ai.loadmodel(cmd[1])
            print(f"Loaded {cmd[1]}")
        elif cmd[0] == "undo":
            if ai.undo():
                print("Undo successful.")
            else:
                print("Undo failed.")
        elif cmd[0] == "redo":
            if ai.redo():
                print("Redo successful.")
            else:
                print("Redo failed.")
        elif cmd[0] == "chat":
            prompt = ' '.join(cmd[1:])
            if not prompt:
                print("Provide a prompt.")
                continue
            print(ai.chat(prompt))
        elif cmd[0] == "status":
            print(f"Trained: {ai.trained}")
            print(f"History length: {len(ai.history)}, current index: {ai.current}")
        elif cmd[0] == "exit":
            break
        else:
            print("Unknown command. Type 'help'.")

if __name__ == "__main__":
    main()
