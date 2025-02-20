import configparser
import google.generativeai as genai


MODEL_NAME = 'gemini-2.0-flash'
CONFIG_FILEPATH = 'config.ini'
GENERATION_CONFIG = {
  'temperature': 1,
  'top_p': 0.95,
  'top_k': 0,
  'max_output_tokens': 16192,
}
SAFETY_SETTINGS = [
  {
    'category': 'HARM_CATEGORY_HARASSMENT',
    'threshold': 'BLOCK_MEDIUM_AND_ABOVE'
  },
  {
    'category': 'HARM_CATEGORY_HATE_SPEECH',
    'threshold': 'BLOCK_MEDIUM_AND_ABOVE'
  },
  {
    'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
    'threshold': 'BLOCK_MEDIUM_AND_ABOVE'
  },
  {
    'category': 'HARM_CATEGORY_DANGEROUS_CONTENT',
    'threshold': 'BLOCK_MEDIUM_AND_ABOVE'
  },
]
SYSTEM_INSTRUCTION_FILEPATH = 'system_instructions/mimisbrunnr.txt'


def run_setup():
    config_parser = configparser.ConfigParser()
    config_parser.read(CONFIG_FILEPATH)
    config = config_parser['config']

    genai.configure(api_key=config['GOOGLE_AI_API_KEY'])


def list_models() -> None:
    print('LIST OF MODELS \n')
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)


def file_reader(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print("Pure Exception:", e)


def get_model(model=MODEL_NAME,
              generation_config=GENERATION_CONFIG,
              safety_settings=SAFETY_SETTINGS,
              system_instruction=file_reader(SYSTEM_INSTRUCTION_FILEPATH)):
    return genai.GenerativeModel(model_name=model,
                                 generation_config=generation_config,
                                 safety_settings=safety_settings,
                                 system_instruction=system_instruction)


def simple_text_generator(prompt):
    model = get_model()
    response = model.generate_content(prompt)
    return response.text


def write_output(content, file_extension='.md'):
    with open('output'+file_extension, 'w', encoding='utf-8') as f:
        f.write(content)


def input_text_generator():
    prompt = input('Sobre o que você deseja obter conhecimento?: ')
    result = simple_text_generator(prompt)
    print(result)


run_setup()
input_text_generator()