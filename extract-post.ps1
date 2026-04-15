$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open("C:\Users\marcenuk\Desktop\Новый проект\Пост для линкедин 1.docx", $false, $true)
$text = $doc.Content.Text
$doc.Close($false)
$word.Quit()
Write-Output $text
