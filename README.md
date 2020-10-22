# nscrapy


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
