import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

def download_image(url, filename):
    """Baixa uma imagem de uma URL e a salva em um arquivo."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status() # Levanta um erro para códigos de status HTTP ruins (4xx ou 5xx)
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Baixado: {filename}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar {url}: {e}")
        return False

def create_image_subplot(start_year, end_year, images_per_row, output_filename="subplot_funceme_chuva_jan_1974_2026.png", main_title="", logo_path=None):
    """
    Cria uma imagem de subplot combinando imagens de um intervalo de anos.

    Args:
        start_year (int): O ano de início.
        end_year (int): O ano final.
        images_per_row (int): Número de imagens por linha no subplot.
        output_filename (str): Nome do arquivo da imagem de saída.
        main_title (str): Título principal para a imagem combinada.
    """
    base_url = "http://www5.funceme.br/web/storage/obs/interpolation_kriging_funceme_valid_rain/{}/1/category-pr-jan-{}.png"

    image_paths = []
    temp_dir = "temp_funceme_images"
    os.makedirs(temp_dir, exist_ok=True)

    print(f"Baixando imagens de {start_year} a {end_year}...")
    for year in range(start_year, end_year + 1):
        url = base_url.format(year, year)
        #filename = os.path.join(temp_dir, f"category-pr-fev-mai-{year}.png")
        filename = os.path.join(temp_dir, f"category-pr-jan-{year}.png")
        if download_image(url, filename):
            image_paths.append(filename)

    if not image_paths:
        print("Nenhuma imagem foi baixada com sucesso. Não é possível criar o subplot.")
        return

    num_images = len(image_paths)
    num_rows = (num_images + images_per_row - 1) // images_per_row #

    # Ajuste do figsize para um layout mais compacto, mantendo a proporção
    # 3.5 foi um bom ponto de partida, vamos diminuir para 2.5 ou 3 para menos espaço entre
    fig, axes = plt.subplots(num_rows, images_per_row, figsize=(images_per_row * 2.6, num_rows * 2.9))
    axes = axes.flatten() # Achata o array de eixos para fácil iteração

    print("Construindo a imagem do subplot...")

    for i, img_path in enumerate(image_paths):
        img = mpimg.imread(img_path)
        axes[i].imshow(img)
        axes[i].set_title(os.path.basename(img_path).replace('category-pr-jan-', '').replace('.png', ''), fontsize=14)
        axes[i].axis('off') # Remove os eixos para uma visualização mais limpa
#    axes.annotate(0.9,0.1,'Climatolgioia')
    # Oculta subplots vazios, se houver
    for i in range(num_images, len(axes)):
        fig.delaxes(axes[i])

    # Adiciona o título principal
    if main_title:
        # Ajuste o 'y' para mover o título para baixo. 0.95 é um bom valor inicial.
        fig.suptitle(main_title, fontsize=24, y=0.935)
    fig.text(0.885, 0.156, '*Climatologia 1981-2010', fontsize=18,
horizontalalignment='right', verticalalignment='bottom', transform=fig.transFigure)

    if logo_path and os.path.exists(logo_path):
        logo = mpimg.imread(logo_path)
        # Cria um novo eixo para a logo. As coordenadas [left, bottom, width, height] são relativas à figura.

        logo_ax = fig.add_axes([0.66, 0.13, 0.09, 0.08]) # Posiciona no canto inferior direito, ajuste conforme necessário
        logo_ax.imshow(logo)
        logo_ax.axis('off') # Desliga os eixos do subplot da logo

    # Ajusta o espaçamento entre subplots. Valores menores significam menos espaço.
    plt.subplots_adjust(wspace=0.09, hspace=0.14)
    plt.savefig(output_filename, bbox_inches='tight') # bbox_inches='tight' ajuda a evitar o corte do título


    print(f"Imagem combinada salva como: {output_filename}")



    # Limpar as imagens baixadas
    for img_path in image_paths:
        os.remove(img_path)
    os.rmdir(temp_dir)
    print(f"Imagens temporárias removidas de {temp_dir}")

if __name__ == "__main__":
    start_year = 1974
    end_year = 2026
    images_per_row = 10
    logo_file='logo_funceme.png'
    #main_title = "Histórico de categoria de precipitação Fev a Maio de 1974 a 2025"
    main_title = "Histórico de categoria de precipitação Jan de 1974 a 2026*"
    create_image_subplot(start_year, end_year, images_per_row, main_title=main_title,
                        logo_path=logo_file)
