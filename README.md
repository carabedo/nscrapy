# nscrapy


Libreria para bajar notas de clarin y pagina 12, solo se necesita la URL.

Ejemplo:

```python
import nscrap as ns
nota1=ns.clarin('url de la nota de clarin)
nota1.get()
```

Luego el objeto nota1 tiene los siguientes atributos:


* nota.titulo : titulo de la nota
* nota.com : comentarios
* nota.volanta : volanta de la nota
* nota.bajada : resumen o subtitulo
* nota.cuerpo : cuerpo nota
* nota.bold : texto en negrita
