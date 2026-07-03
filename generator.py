def generate(prompt, modality):
    if modality == "code":
        return "This Ai Have Not Been Trained For Coding Yet."
    elif modality == "audio":
        return "This Ai Have Not Been Trained For Audio Gen Yet."
    elif modality == "video":
        return "This Ai Have Not Been Trained For Video Gen Yet"
    elif modality == "image":
        return "This Ai Have Not Been Trained for Image Gen Yet"
    else:
        return "Unknown modality."
