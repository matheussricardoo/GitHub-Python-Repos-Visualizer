import requests
import pygal
from pygal.style import LightColorizedStyle, LightenStyle

def fetch_github_data(url):
    """Realiza a chamada à API do GitHub e trata possíveis erros"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lança um erro HTTP se ocorrer um problema
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro na solicitação: {e}")
        return None

def prepare_data(response_dict):
    """Prepara os dados da API para o gráfico"""
    repo_dicts = response_dict['items'][:10]  # Seleciona os 10 primeiros repositórios

    repo_names, star_counts, descriptions, urls = [], [], [], []
    for repo in repo_dicts:
        # Limita o nome do repositório em 20 caracteres
        repo_names.append(repo['name'][:20] + '...' if len(repo['name']) > 20 else repo['name'])
        star_counts.append(repo['stargazers_count'])
        # Fornece uma descrição do repositório ou uma mensagem padrão se não houver descrição
        descriptions.append(repo['description'] if repo['description'] else 'Sem descrição')
        # Adiciona o link do repositório
        urls.append(repo['html_url'])
    
    return repo_names, star_counts, descriptions, urls

def create_chart(repo_names, star_counts, descriptions, urls):
    """Cria o gráfico com os dados coletados e links interativos"""
    # Define o estilo do gráfico com cores suaves
    my_style = LightenStyle('#7db4e6', base_style=LightColorizedStyle)
    
    # Configura o gráfico de barras
    chart = pygal.Bar(
        style=my_style,
        x_label_rotation=45,  # Rotação das labels do eixo X
        show_legend=False
    )
    
    chart.title = f"Top 10 Repositórios Python com mais Estrelas\nTotal de {len(repo_names)} Repo"
    chart.x_labels = repo_names
    
    # Adiciona as barras com a quantidade de estrelas, descrições e links
    chart.add('', [{
        'value': stars,
        'label': f"{desc}\nLink: {url}",
        'xlink': url  # Adiciona o link interativo
    } for stars, desc, url in zip(star_counts, descriptions, urls)])
    
    chart.render_to_file('python_repos.svg')
    print("Gráfico gerado com sucesso: python_repos.svg")

def main():
    """Função principal para execução do script"""
    url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
    
    # Busca os dados da API
    api_response = fetch_github_data(url)
    
    if api_response:
        print(f"Total de repositórios encontrados: {api_response['total_count']}")
        
        # Prepara os dados e cria o gráfico
        repo_names, star_counts, descriptions, urls = prepare_data(api_response)
        create_chart(repo_names, star_counts, descriptions, urls)
    else:
        print("Não foi possível obter dados da API. Encerrando o script...")

if __name__ == "__main__":
    main()