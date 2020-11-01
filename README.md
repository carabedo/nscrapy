<div align="center">
  <h1> NSCRAPY: Scraper de principales portales de noticias argentinos.</h1>
  <a class="header-badge" target="_blank" href="https://www.linkedin.com/in/carabedo/">
  <img src="https://img.shields.io/badge/style--5eba00.svg?label=LinkedIn&logo=linkedin&style=social">
  </a>
  <a class="header-badge" target="_blank" href="https://twitter.com/muydipalma">
  <img alt="Twitter Follow" src="https://img.shields.io/twitter/follow/muydipalma?style=social">
  </a>

<sub>Author:
<a href="https://www.linkedin.com/in/carabedo/" target="_blank">Fernando Carabedo</a><br>
<small> Octubre, 2020</small>
</sub>



</div>
</div>

<div>
<p align="center">
<a href='https://cafecito.app/carabedo' rel='noopener' target='_blank'><img srcset='https://cdn.cafecito.app/imgs/buttons/button_2.png 1x, https://cdn.cafecito.app/imgs/buttons/button_2_2x.png 2x, https://cdn.cafecito.app/imgs/buttons/button_2_3.75x.png 3.75x' src='https://cdn.cafecito.app/imgs/buttons/button_2.png' alt='Invitame un café en cafecito.app' /></a>
</p>
</div>

Libreria para bajar notas de clarin , pagina12, cronica y cronista.

Instalacion:

```python
pip install nscrapy
``` 



```python
clarin()
p12()
cronica()
cronista()
``` 

Ejemplo de uso, scrapear notas de hoy (para pagina 12 cambiar clarin por p12) con comentarios:

```python
from nscrapy import nscrap as ns
from nscrapy.clarin import get

notasclarin=ns.clarin()

#scrapeo el portal
notasclarin.hoy()

#las urls a las notas de hoy estan en .urls

notashoy=get(notasclarin.urls)

```
notashoy es una lista de objetos nota:

`nota.titulo`  titulo de la nota

`nota.comm`  comentarios

`nota.com`  ' '.join(comentarios)

`nota.volanta`  volanta de la nota

`nota.bajada`  resumen o subtitulo

`nota.cuerpo`  cuerpo nota

`nota.bolds`  textos en negrita

`nota.bold`  ' '.join(bolds)


