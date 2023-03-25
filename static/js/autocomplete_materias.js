new Autocomplete('#autocomplete', {
        
    search: input => {
        const url = `/clases/buscar-clase/?clase=${(input)}`
        return new Promise(resolve => {
            fetch(url)
            .then(response => response.json())
            .then(data => {
                resolve(data.data)
            })
        })
    },
    renderResult: (result, props) => {
        return `
        <li ${props}>
            <div class="wiki-title">
                ${result.ciclo} ${result.materia} ${result.docente}
            </div>
            
        </li>
        `
    },
    getResultValue: result => result.materia,
    onSubmit: result => {
        const div = document.getElementById('form-group')
        const element = document.createElement('div')
        elementInput = document.getElementById('id_clase')
        // verify if elementInput is not null
        if (elementInput) {
            elementInput.setAttribute('value',result.id)
        }else {
            elementInput = `<input type="hidden" name="id_clase" id="id_clase" value="${result.id}">`
            element.innerHTML = elementInput
            div.appendChild(element)
        }
        const nombreMateriaInput = document.getElementById('nombre_materia_input')
        nombreMateriaInput.setAttribute('value',"${result.ciclo} ${result.materia}")
    }
})