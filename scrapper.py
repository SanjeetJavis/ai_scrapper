from googleapiclient.discovery import build
import requests
from bs4 import BeautifulSoup
import openai
import json

openai.api_key = #
api_key = #
cse_id = #
country_code = 'countryIN'
time_restriction = 'h24'


def google_search(search_terms, api_key, cse_id, site_search, country_code, time_restriction):
    query = ' OR '.join(search_terms)

    # Build a service object for interacting with the API
    service = build("customsearch", "v1", developerKey=api_key)

    # Execute the search request using the specified parameters, including country and time restrictions
    res = service.cse().list(q=query, cx=cse_id, siteSearch=site_search, cr=country_code, dateRestrict=time_restriction).execute()

    return res.get('items', [])


def get_text_from_url(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        # Remove script and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        # Get text
        text = soup.get_text(separator=' ', strip=True)
        return text
    except Exception as e:
        print(f"Could not fetch text from {url}: {e}")
        return ""


def is_document_relevant(title, document_text, theme):
    prompt = f"The following document is provided for analysis:\n\n{title}\n\n{document_text}\n\nIs this document primarily talking about {theme}?"

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=100,
        temperature=0
    )
    answer = response.choices[0].text.strip().lower()
    print(prompt)
    print(answer)
    if "yes" in answer:
        return True
    elif "no" in answer:
        return False
    else:
        return "Uncertain"


def extract_structured_data(title, document_text, theme, questions):
    sys_prompt = f"Following is a news article on the theme \"{theme}\"::\n\n{title}\n\n{document_text}\n\n"
    questions_prompt = "Read the above article and answer the following questions and output a JSON: \n\n"
    for i, question in enumerate(questions):
        questions_prompt = questions_prompt + f"{i}. {question}\n"
    messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": questions_prompt}
        ]
    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=500,
        temperature=0,
        response_format={"type": "json_object"}
    )
    answer = completions.choices[0].message.content
    print(messages)
    print(answer)
    answer = json.loads(answer)
    print(messages)
    print(answer)
    return answer


def controller(sites, keywords, theme, questions):
    results_store = []
    # Iterate over each site and keyword, and perform a search
    for site in sites:
        results = google_search(keywords, api_key, cse_id, site, country_code, time_restriction)
        for result in results:
            text = get_text_from_url(result['link'])
            text = text[0: min([3000, len(text)])]
            results_store.append({'Title': result['title'],
                           'Link': result['link'],
                           'Text': text})

            print(f"Title: {result['title']}\nLink: {result['link']}\n")


    # Filter Junk
    results_store_junk_filtered = []
    for result in results_store:
        is_relevant = is_document_relevant(result['Title'], result['Text'], theme=theme)
        if is_relevant == True:
            results_store_junk_filtered.append(result)

    # Extract Data
    structured_data = []
    for result in results_store_junk_filtered:
        sd = extract_structured_data(result['Title'], result['Text'], theme, questions)
        sd['article_link'] = result['Link']
        sd['article_title'] = result['Title']
        structured_data.append(sd)

    return structured_data

