# Definir la ruta del archivo origen
$sourceFile = "C:/Folder/file.txt"

# Definir la carpeta de destino
$destinationFolder = "C:/Backups"

# Definir la ruta del archivo de log
$logFile = "C:/Backups/copy_log.txt"

# Obtener la fecha y hora actual en formato dd-mm-yyyy_hh-mm-ss ( se utilizará tanto en el nombre del archivo, como en el log de ejecuciones )
$timestamp = Get-Date -Format "dd-MM-yyyy_HH-mm-ss"

# Definir la ruta del archivo de destino con la fecha y hora añadidas
$destinationFile = Join-Path $destinationFolder "file-$timestamp.txt"

# Manejo de errores
try {
    # Comprobar si el archivo de origen existe
    if (!(Test-Path -Path $sourceFile)) {
        throw "El archivo origen no existe: $sourceFile"
    }

    # Comprobar si la carpeta de destino existe, crearla si no existe
    if (!(Test-Path -Path $destinationFolder)) {
        New-Item -ItemType Directory -Path $destinationFolder -Force | Out-Null
    }

    # Intentar copiar el archivo
    Copy-Item -Path $sourceFile -Destination $destinationFile -Force

    # Si la copia es exitosa, escribir mensaje en el archivo de log
    $logMessage = "$logTimestamp - Éxito: Archivo copiado a $destinationFile"
    Add-Content -Path $logFile -Value $logMessage
} catch {
    # Si ocurre un error, escribir el mensaje de error en el archivo de log
    $logMessage = "$timestamp - Error: $_"
    Add-Content -Path $logFile -Value $logMessage
}
