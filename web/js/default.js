//v20230520-1720

var notas = ['Do', 'Re', 'Mi', 'Fa', 'Sol', 'La', 'Si'];
var audioInicio = ["bienvenida.mp3", "inicio.mp3"]
var audioFin = ["fin.mp3"]

var notasGeneradas = []; // Arreglo para almacenar las notas generadas
var notasmp3 = notas.map(function(nota, indice) {
    var numero = ('0' + indice).slice(-2); // Añade un cero al principio y toma los últimos dos caracteres
    return numero + '-' + nota.toLowerCase() + '.mp3';
});

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('btn-aumentar').addEventListener('click', function () {
        var numeroNotasInput = document.getElementById('numero-notas');
        numeroNotasInput.value = parseInt(numeroNotasInput.value) + 1;
    });

    document.getElementById('btn-disminuir').addEventListener('click', function () {
        var numeroNotasInput = document.getElementById('numero-notas');
        if (parseInt(numeroNotasInput.value) > 1) {
            numeroNotasInput.value = parseInt(numeroNotasInput.value) - 1;
        }
    });

    document.getElementById('btn-aumentar-tiempo').addEventListener('click', function () {
        var tiempoNotasInput = document.getElementById('tiempo-notas');
        if (parseInt(tiempoNotasInput.value) < 15.0) {
            tiempoNotasInput.value = (parseFloat(tiempoNotasInput.value) + .1).toFixed(1);
        }
    });

    document.getElementById('btn-disminuir-tiempo').addEventListener('click', function () {
        var tiempoNotasInput = document.getElementById('tiempo-notas');
        if (parseInt(tiempoNotasInput.value) > 0.5) {
            tiempoNotasInput.value = (parseFloat(tiempoNotasInput.value) - .1).toFixed(1);
        }
    });

    document.getElementById('btn-iniciar').addEventListener('click', function () {
        var numeroNotas = document.getElementById('numero-notas').value;
        if (numeroNotas === '' || isNaN(numeroNotas) || parseInt(numeroNotas) >= 100) {
            alert('Error: El número debe ser un entero menor a 100.');
            return;
        }
        iniciarDictado()
        reproducirDictado()

        var btnMostrarOcultar = document.getElementById('btn-mostrar-ocultar');
        btnMostrarOcultar.style.display = 'inline-block';
        btnMostrarOcultar.textContent = 'Mostrar Dictado';
        

        var btnDictar = document.getElementById('btn-dictar');
        btnDictar.style.display = 'inline-block';

        btnDictar.addEventListener('click', function() {
            reproducirDictado()
        });

        var btnDescargar = document.getElementById('btn-descargar');
        btnDescargar.style.display = 'inline-block';


        btnDescargar.addEventListener('click', function () {
            var resultadoDiv = document.getElementById('resultado');
            var aElement = document.createElement('a');
            aElement.href = generarTextoDescarga(resultadoDiv);
            aElement.download = 'dictado_notas.txt';
            aElement.click();
        });

    });

    document.getElementById('btn-mostrar-ocultar').addEventListener('click', function () {
        var notasElement = document.getElementById('resultado').getElementsByTagName('p');

        if (this.textContent === 'Mostrar Dictado') {
            for (var i = 0; i < notasElement.length; i++) {
                notasElement[i].style.display = 'block';
            }
            this.textContent = 'Ocultar Dictado';
        } else {
            for (var i = 0; i < notasElement.length; i++) {
                notasElement[i].style.display = 'none';
            }
            this.textContent = 'Mostrar Dictado';
        }
    });

    function generarNotasAleatorias() {
        var numeroNotas = parseInt(document.getElementById('numero-notas').value);
        notasGeneradas = []; // Limpiar el arreglo de notas generadas
      
        for (var i = 0; i < numeroNotas; i++) {
          var randomIndex = Math.floor(Math.random() * notas.length);
          notasGeneradas.push(notas[randomIndex]);
        }
      
        return notasGeneradas;
      }

    function getAudioSources() {
        let audioSources = []
        let current_url = window.location.href;
        let path = current_url.substring(0, current_url.lastIndexOf('/'));
        let url = path + '/audios/'

        for (var i = 0; i < audioInicio.length; i++) {
            let src = url + audioInicio[i]
            audioSources.push(src);
        }

        for (var i = 0; i < notasGeneradas.length; i++) {
            let indice = notas.indexOf(notasGeneradas[i])
            let src = url + notasmp3[indice]
            audioSources.push(src);
        }

        for (var i = 0; i < audioFin.length; i++) {
            let src = url + audioFin[i]
            audioSources.push(src);
        }

        return audioSources
    }

    function iniciarDictado() {
        generarNotasAleatorias();

        var resultadoDiv = document.getElementById('resultado');
        resultadoDiv.innerHTML = '<h2>Pulsa el bot&oacute;n para Mostrar el dictado</h2>';
        
        var notasElement = document.createElement('p');
        notasElement.textContent = notasGeneradas.join(' ');
        resultadoDiv.appendChild(notasElement);

        var notasContainer = document.querySelector('.notas-container');
        notasContainer.innerHTML = '';
      
        var anchoNota = 100 / notasGeneradas.length; // Calcula el ancho de cada nota

        for (var i = 0; i < notasGeneradas.length; i++) {
          var notaElement = document.createElement('div');
          notaElement.className = 'nota';
          notaElement.style.width = anchoNota + '%'; // Aplica el ancho a cada nota
          var notaLabel = document.createElement('div');
          notaLabel.className = 'nota-label';
          notaLabel.textContent = notasGeneradas[i];
          notaElement.appendChild(notaLabel);
          notasContainer.appendChild(notaElement);
        }


    }

    function reproducirDictado() {
        var audioPlayer = document.getElementById('audioPlayer');
        var tiempoEntreNotas = document.getElementById('tiempo-notas').value * 1000;
    
        if (audioPlayer) {
            audioPlayer.parentNode.removeChild(audioPlayer);
        }
        
        audioPlayer = document.createElement('audio');
        audioPlayer.setAttribute('id', 'audioPlayer');
        audioPlayer.setAttribute('autoplay', 'autoplay');
    
        var sources = getAudioSources();
    
        var currentIndex = 0;
        audioPlayer.addEventListener('ended', function() {
            if (currentIndex < audioInicio.length) {
                duracion = 0
            } else {
                duracion = tiempoEntreNotas
            }
            setTimeout(function() {
                currentIndex++;
                if (currentIndex < sources.length) {
                    audioPlayer.src = sources[currentIndex];
                    audioPlayer.play();
                }
            }, duracion);
        });
    
        audioPlayer.src = sources[currentIndex];
        document.body.appendChild(audioPlayer);
    
        audioPlayer.play(); // Reproduce el primer origen automáticamente
    }

    function generarTextoDescarga(elemento) {
        var textoDescarga = '';
        for (var i = 0; i < notasGeneradas.length; i++) {
            textoDescarga += notasGeneradas[i] + '\n';
        }
        return 'data:text/plain;charset=utf-8,' + encodeURIComponent(textoDescarga);
    }

});
