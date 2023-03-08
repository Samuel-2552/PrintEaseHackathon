# Set the printer name
$printerName = "EPSON L310 Series"

# Set the file path and name
$filePath = "'D://College//iquest//File-Upload//sample.pdf'"

# Set the number of copies, duplex mode, and color mode
$printCopies = 2
$printDuplex = "LongEdge"
$printColor = "Color"

# Create a new PrinterSettings object
$printerSettings = New-Object System.Drawing.Printing.PrinterSettings
$printerSettings.PrinterName = $printerName
$printerSettings.Copies = $printCopies
$printerSettings.Duplex = [System.Drawing.Printing.Duplex]::$printDuplex

# Create a new PrintDocument object
$printDocument = New-Object System.Drawing.Printing.PrintDocument
$printDocument.PrinterSettings = $printerSettings

# Set the print color mode
if ($printColor -eq "Color") {
    $printDocument.DefaultPageSettings.Color = $true
} else {
    $printDocument.DefaultPageSettings.Color = $false
}

# Print the file
$printDocument.DocumentName = $filePath
$printDocument.Print()
