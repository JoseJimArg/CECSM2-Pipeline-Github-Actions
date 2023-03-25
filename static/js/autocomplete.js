new Autocomplete('#autocomplete', {
        
    search: input => {
        const url = `/materias/buscar-docente/?docente=${(input)}`
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
                ${result.first_name} ${result.last_name}
            </div>
            
        </li>
        `
    },
    getResultValue: result => result.matricula,
    onSubmit: result => {
        const div = document.getElementById('form-group')
        const element = document.createElement('div')
        elementInput = document.getElementById('id_docente')
        
        // verify if elementInput is not null
        if (elementInput) {
            elementInput.setAttribute('value',result.id)
        }else {
            elementInput = `<input type="hidden" name="id" id="id_docente" value="${result.id}">`
            element.innerHTML = elementInput
            div.appendChild(element)
        }
        const matriculaInput = document.getElementById('matricula_input')
        matriculaInput.setAttribute('value',result.matricula)
    }
})