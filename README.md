<div align="center">
  <h1> 30 Days Of JavaScript: Introduction</h1>
  <a class="header-badge" target="_blank" href="https://www.linkedin.com/in/asabeneh/">
  <img src="https://img.shields.io/badge/style--5eba00.svg?label=LinkedIn&logo=linkedin&style=social">
  </a>
  <a class="header-badge" target="_blank" href="https://twitter.com/Asabeneh">
  <img alt="Twitter Follow" src="https://img.shields.io/twitter/follow/asabeneh?style=social">
  </a>

<sub>Author:
<a href="https://www.linkedin.com/in/asabeneh/" target="_blank">Asabeneh Yetayeh</a><br>
<small> January, 2020</small>
</sub>

  <div>

🇬🇧 [English](./readMe.md)
🇪🇸 [Spanish](./Spanish/readme.md)
🇷🇺 [Russian](./RU/README.md)

  </div>

</div>
</div>

<div>

<small>Support [**Asabeneh**](https://www.patreon.com/asabeneh?fan_landing=true) to create more educational materials</small>  
[<img src = './images/become_patreon.png' alt='become-asabeneh-patreon' title='click' />](https://www.patreon.com/asabeneh?fan_landing=true)

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
