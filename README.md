# Django Elasticsearch Integration Project

This project demonstrates how to integrate Elasticsearch with Django for full-text search functionality. It uses the `django-elasticsearch-dsl` package to connect Django models with Elasticsearch and perform advanced search queries.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Install Elasticsearch](#install-elasticsearch)
- [Set Up Django Project](#set-up-django-project)
- [Configure Elasticsearch in Django](#configure-elasticsearch-in-django)
- [Indexing Data](#indexing-data)
- [Running the Project](#running-the-project)
- [Search Functionality](#search-functionality)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before starting, ensure you have the following installed:

- Python 3.8+
- Django 4.0+
- Elasticsearch 8.x
- Ubuntu/Debian (for Elasticsearch installation)

## Install Elasticsearch

Follow these steps to install Elasticsearch on Ubuntu/Debian:

1. **Install Elasticsearch**

    Download and install the Elasticsearch Debian package:

    ```bash
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.13.0-amd64.deb
    sudo dpkg -i elasticsearch-8.13.0-amd64.deb
    ```

2. **Configure Elasticsearch to start automatically on boot:**

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable elasticsearch
    sudo systemctl start elasticsearch
    ```

3. **Verify Elasticsearch is running:**

    ```bash
    curl -X GET "localhost:9200?pretty"
    ```

    You should see a response like:

    ```json
    {
      "name": "your-hostname",
      "cluster_name": "elasticsearch",
      "cluster_uuid": "abc123",
      "version": {
        "number": "8.13.0",
        "build_flavor": "default",
        "build_type": "deb",
        "build_hash": "abc123",
        "build_date": "2025-03-12T00:00:00.000Z",
        "build_snapshot": false,
        "lucene_version": "9.10.0",
        "minimum_wire_compatibility_version": "7.17.0",
        "minimum_index_compatibility_version": "7.0.0"
      },
      "tagline": "You Know, for Search"
    }
    ```

4. **Secure Elasticsearch**

    Generate passwords for built-in users:

    ```bash
    sudo /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
    ```

    Configure TLS for secure communication:

    ```bash
    sudo /usr/share/elasticsearch/bin/elasticsearch-certutil ca
    sudo /usr/share/elasticsearch/bin/elasticsearch-certutil cert --ca elastic-stack-ca.p12
    ```

    Update the Elasticsearch configuration file (`/etc/elasticsearch/elasticsearch.yml`) with the following:

    ```yaml
    network.host: 127.0.0.1
    http.port: 9200
    discovery.type: single-node

    xpack.security.enabled: true
    xpack.security.transport.ssl.enabled: true
    xpack.security.http.ssl.enabled: true
    xpack.security.transport.ssl.keystore.path: /etc/elasticsearch/elastic-certificates.p12
    xpack.security.transport.ssl.truststore.path: /etc/elasticsearch/elastic-certificates.p12
    ```

    Restart Elasticsearch:

    ```bash
    sudo systemctl restart elasticsearch
    ```

## Set Up Django Project

1. **Clone the repository:**

    ```bash
    git https://github.com/snipher-marube/techblog.git
    cd techblog
    ```

2. **Create a virtual environment:**

    ```bash
    python3 -m venv .env
    source .env/bin/activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run migrations:**

    ```bash
    python manage.py migrate
    ```

## Configure Elasticsearch in Django

1. **Install django-elasticsearch-dsl:**

    ```bash
    pip install django-elasticsearch-dsl
    ```

2. **Add django_elasticsearch_dsl to your INSTALLED_APPS in settings.py:**

    ```python
    INSTALLED_APPS = [
        ...
        'django_elasticsearch_dsl',
    ]
    ```

3. **Configure Elasticsearch settings in settings.py:**

    ```python
    ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'http://user:password@localhost:9200'
        }
    }
    ```

4. **Define your Elasticsearch document in documents.py:**

    ```python
    from django_elasticsearch_dsl import Document, fields
    from django_elasticsearch_dsl.registries import registry
    from .models import Post

    @registry.register_document
    class PostDocument(Document):
        class Index:
            name = 'posts'
            settings = {
                'number_of_shards': 1,
                'number_of_replicas': 0,
            }

        class Django:
            model = Post
            fields = [
                'title',
                'body',
                'intro',
                'slug',
                'image',
                'publish',
            ]
    ```

## Indexing Data

1. **Build the Elasticsearch index:**

    ```bash
    python manage.py search_index --rebuild
    ```

2. **Add new data to the index automatically by saving your Django models.**

## Running the Project

1. **Start the Django development server:**

    ```bash
    python manage.py runserver
    ```

2. **Access the search functionality at `http://127.0.0.1:8000/search/`.**

## Search Functionality

The search view uses Elasticsearch to perform full-text search with relevance sorting. Example query:

```python
search = PostDocument.search().query(
    'multi_match', 
    query='your search term',
    fields=['title^3', 'body^2', 'intro'],
    fuzziness='AUTO'
)
results = search.to_queryset()
```

## Troubleshooting

1. **Elasticsearch Not Running**

    Check the status: 

    ```bash
    sudo systemctl status elasticsearch
    ```

    View logs: 

    ```bash
    sudo journalctl -u elasticsearch
    ```

2. **Connection Errors**

    Verify Elasticsearch is accessible: 

    ```bash
    curl -X GET "localhost:9200?pretty"
    ```

    Check Django settings for correct host, port, and credentials.

3. **Indexing Issues**

    Rebuild the index: 

    ```bash
    python manage.py search_index --rebuild
    ```

    Check if the index exists: 

    ```bash
    curl -X GET "localhost:9200/posts?pretty"
    ```

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository.**

2. **Create a new branch:**

    ```bash
    git checkout -b feature/your-feature
    ```

3. **Commit your changes:**

    ```bash
    git commit -m 'Add some feature'
    ```

4. **Push to the branch:**

    ```bash
    git push origin feature/your-feature
    ```

5. **Submit a pull request.**

## License

This project is licensed under the MIT License. See the LICENSE file for details.