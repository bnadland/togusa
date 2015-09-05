# Togusa Textanalysis Api

## /api/language - Language detection

    $ curl -H "Content-Type: application/json" -X POST \
      -d '{"text": "The Aneristic Principle is that of apparent order; the Eristic Principle is that of apparent disorder."}' \
      127.0.0.1:5000/api/language
    {
      "lang": "en",
      "probabilities": [
        "en",
        1.0
      ],
      "text": "The Aneristic Principle is that of apparent order; the Eristic Principle is that of apparent disorder."
    }
        
## /api/keywords - Keyword extraction

    $ curl -H Content-Type: application/json -X POST \
      -d '{"text": "The Aneristic Principle is that of apparent order; the Eristic Principle is that of apparent disorder."}' \
      127.0.0.1:5000/api/keywords
    {
      "keywords": [
        "aneristic principle",
        "apparent order",
        "eristic principle",
        "apparent disorder"
      ],
      "lang": "en",
      "text": "The Aneristic Principle is that of apparent order; the Eristic Principle is that of apparent disorder."
    }
