# Trading Bot - GitHub'a Hızlı Deploy Script
# PowerShell'de çalıştır: .\deploy.ps1

Write-Host "🚀 Trading Bot GitHub Deploy" -ForegroundColor Green
Write-Host ""

# Git kurulu mu kontrol et
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git kurulu değil!" -ForegroundColor Red
    Write-Host "Git'i buradan indir: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit
}

Write-Host "✅ Git kurulu" -ForegroundColor Green

# GitHub kullanıcı adı iste
Write-Host ""
$username = Read-Host "GitHub kullanıcı adın"

# Repo adı iste
Write-Host ""
$reponame = Read-Host "Repo adı (varsayılan: trading-bot)"
if ([string]::IsNullOrWhiteSpace($reponame)) {
    $reponame = "trading-bot"
}

Write-Host ""
Write-Host "📦 Git repository başlatılıyor..." -ForegroundColor Cyan

# Git init
if (-not (Test-Path ".git")) {
    git init
    Write-Host "✅ Git başlatıldı" -ForegroundColor Green
} else {
    Write-Host "⚠️  Git zaten başlatılmış" -ForegroundColor Yellow
}

# Git add
Write-Host ""
Write-Host "📝 Dosyalar ekleniyor..." -ForegroundColor Cyan
git add .
Write-Host "✅ Dosyalar eklendi" -ForegroundColor Green

# Git commit
Write-Host ""
Write-Host "💾 Commit yapılıyor..." -ForegroundColor Cyan
git commit -m "Initial commit - Trading Bot"
Write-Host "✅ Commit yapıldı" -ForegroundColor Green

# Branch
Write-Host ""
Write-Host "🌿 Branch ayarlanıyor..." -ForegroundColor Cyan
git branch -M main
Write-Host "✅ Branch: main" -ForegroundColor Green

# Remote ekle
Write-Host ""
Write-Host "🔗 GitHub remote ekleniyor..." -ForegroundColor Cyan
$remoteUrl = "https://github.com/$username/$reponame.git"
git remote remove origin 2>$null
git remote add origin $remoteUrl
Write-Host "✅ Remote eklendi: $remoteUrl" -ForegroundColor Green

# Push
Write-Host ""
Write-Host "⬆️  GitHub'a push ediliyor..." -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  GitHub kullanıcı adı ve token isteyecek!" -ForegroundColor Yellow
Write-Host "Token oluştur: https://github.com/settings/tokens" -ForegroundColor Yellow
Write-Host ""

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Push başarılı!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🎉 Tebrikler! Proje GitHub'a yüklendi!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Sonraki adımlar:" -ForegroundColor Cyan
    Write-Host "1. https://render.com adresine git" -ForegroundColor White
    Write-Host "2. GitHub ile giriş yap" -ForegroundColor White
    Write-Host "3. 'New +' → 'Web Service' seç" -ForegroundColor White
    Write-Host "4. '$reponame' repo'sunu seç" -ForegroundColor White
    Write-Host "5. Environment variables ekle (.env dosyasındaki değerler)" -ForegroundColor White
    Write-Host "6. Deploy et!" -ForegroundColor White
    Write-Host ""
    Write-Host "📖 Detaylı rehber: RENDER_DEPLOY.md" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "❌ Push başarısız!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Olası sebepler:" -ForegroundColor Yellow
    Write-Host "- GitHub'da repo oluşturmadın" -ForegroundColor White
    Write-Host "- Token yanlış" -ForegroundColor White
    Write-Host "- İnternet bağlantısı yok" -ForegroundColor White
    Write-Host ""
    Write-Host "Çözüm:" -ForegroundColor Yellow
    Write-Host "1. https://github.com/new adresine git" -ForegroundColor White
    Write-Host "2. Repo adı: $reponame" -ForegroundColor White
    Write-Host "3. 'Create repository' tıkla" -ForegroundColor White
    Write-Host "4. Bu scripti tekrar çalıştır" -ForegroundColor White
}

Write-Host ""
Read-Host "Devam etmek için Enter'a bas"
