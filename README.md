# lastfm

Este projeto foi desenvolvido para fixar os aprendizados da leitura do capítulo 6 do livro [Designing Cloud Data Platforms](https://www.manning.com/books/designing-cloud-data-platforms), Real-time data processing and analytics, que eu li com pessoas muito queridas no Clube do livro do Jusbrasil ❤️

Aqui tem explicações sobre a arquitetura do projeto, aqui o que eu achei mais importante no capítulo, e aqui o site onde aparece a música que eu estou ouvindo enquanto eu estou ouvindo.

## Como rodar o projeto

Pré-requisitos:

* Docker
* Conta no Lastfm configurada para registrar scrobbles
* Acesso à API Lastfm
* Conta na Google Cloud Platform (GCP)
* Conta de serviço GCP com papel de Editor

Passo a passo pós clone do repositório:

1° Executa containers airflow/streamlit do `docker-compose.yaml`:

```
docker compose up
```

2° Adiciona as variáveis usadas no código na UI do airflow:

* `project_id`: ID do projeto GCP
* `lastfm_username`: nome de usuário da conta Lastfm
* `lastfm_public_key`: key da API Lastfm

3° Adiciona a conta de serviço GCP usada no código na UI do airflow, ela é chamada de `gcp_conn`

4° A url do streamlit é a `http://0.0.0.0:8501`
