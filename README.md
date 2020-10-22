<div align="center">
  <h1> NSCRAPY: Scrapper de principales portales de noticias.</h1>
  <a class="header-badge" target="_blank" href="https://www.linkedin.com/in/fernando-carabedo-76044134/">
  <img src="https://img.shields.io/badge/style--5eba00.svg?label=LinkedIn&logo=linkedin&style=social">
  </a>
  <a class="header-badge" target="_blank" href="https://twitter.com/muydipalma">
  <img alt="Twitter Follow" src="https://img.shields.io/twitter/follow/muydipalma?style=social">
  </a>

<sub>Author:
<a href="https://www.linkedin.com/in/fernando-carabedo-76044134/" target="_blank">Fernando Carabedo</a><br>
<small> Octubre, 2020</small>
</sub>



</div>
</div>

<div>

[![Invitame un café en cafecito.app](https://cdn.cafecito.app/imgs/buttons/button_2.svg)](https://cafecito.app/carabedo)

</div>

Libreria para bajar notas de clarin , pagina12 y cronica.

Solo se necesita la URL.

Ejemplo:

```python
import nscrap as ns
nota1=ns.clarin('url de la nota de clarin)
nota1.get()
```

Luego el objeto nota1 tiene los siguientes atributos:


* nota.titulo : titulo de la nota
* nota.comm : comentarios
* nota.com : ' '.join(comentarios)
* nota.volanta : volanta de la nota
* nota.bajada : resumen o subtitulo
* nota.cuerpo : cuerpo nota
* nota.bolds : textos en negrita
* nota.bold : ' '.join(bolds)
