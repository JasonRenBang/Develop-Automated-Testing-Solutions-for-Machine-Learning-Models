# Develop-Automated-Testing-Solutions-for-Machine-Learning-Models

How to run the project:

1.  Set up a virtual environment: python -m venv openai-env
2.  Activate the virtual environment:
    - Windows: openai-env\Scripts\activate
    - Mac: source openai-env/bin/activate
3.  Install the required packages:
    OpenAI Python Library: pip install openai
    Spacy and Sentence Transformers: pip install spacy sentence-transformers
4.  load the spacy model:
    python -m spacy download en_core_web_md
5.  Set up the OpenAI API key:
    MacOS:
    Open Terminal: You can find it in the Applications folder or search for it using Spotlight (Command + Space).

        Edit Bash Profile: Use the command nano ~/.bash_profile or nano ~/.zshrc (for newer MacOS versions) to open the profile file in a text editor.

        Add Environment Variable: In the editor, add the line below, replacing your-api-key-here with your actual API key: export OPENAI_API_KEY='your-api-key-here'

        Save and Exit: Press Ctrl+O to write the changes, followed by Ctrl+X to close the editor.

        Load Your Profile: Use the command source ~/.bash_profile or source ~/.zshrc to load the updated profile.

        Verification: Verify the setup by typing echo $OPENAI_API_KEY in the terminal. It should display your API key.

    Windows:
    Right-click on 'This PC' or 'My Computer' and select 'Properties'.
    Click on 'Advanced system settings'.
    Click the 'Environment Variables' button.
    In the 'System variables' section, click 'New...' and enter OPENAI_API_KEY as the variable name and your API key as the variable value.

6.  Run the project: demoPrototype.py and the result shows in outcomes.txt
