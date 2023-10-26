## Proyecto de Cálculo de Subredes

Este proyecto es un programa en Python que permite calcular y listar las subredes de una dirección IP dada, junto con sus máscaras de subred correspondientes. A continuación, se describen las principales funciones y características del programa:

- Define funciones para validar direcciones IP y máscaras de subred.
- Proporciona funciones para convertir direcciones IP en formato binario y realizar cálculos relacionados con subredes.
- Solicita al usuario que ingrese una dirección IP y una máscara de subred válidas.
- Permite al usuario especificar si desea calcular subredes en función del número de hosts o del número de subredes.
- Calcula y muestra las subredes resultantes junto con sus máscaras de subred correspondientes.
- Utiliza operaciones binarias para realizar los cálculos necesarios y garantiza que las subredes sean válidas y se ajusten a la dirección IP y la máscara de subred proporcionadas.

Nota: Algunas partes del código están comentadas, y se mencionan líneas de código que están comentadas, por lo que es posible que debas descomentarlas si son necesarias para tu caso de uso específico.

### Ejemplo de Uso:

```
IP (ej:192.168.1.0) : 192.168.1.0
mascara (ej:24 o 255.255.255.0): 255.255.255.0
calcular las subredes usando numero de host por subred (h) o numero de subredes (s): s
numero de subredes : 4
192.168.1.0/26
192.168.1.64/26
192.168.1.128/26
192.168.1.192/26
