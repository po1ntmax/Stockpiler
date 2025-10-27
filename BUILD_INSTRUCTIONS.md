# Build Instructions

This repository includes a GitHub Actions workflow that automatically builds the Stockpiler application using PyInstaller and creates releases with executable files for Windows, macOS, and Linux.

## How to Use

### Manual Build and Release

1. Go to the **Actions** tab in your GitHub repository
2. Select the **Build and Release** workflow
3. Click **Run workflow** button
4. The workflow will:
   - Build the application for all three platforms (Windows, macOS, Linux)
   - Create a new release with version number based on the run number
   - Upload the executable files as release assets

### What Gets Built

The workflow creates:
- **Windows**: `Stockpiler-Windows.zip` - Contains `Stockpiler.exe` and all required files
- **macOS**: `Stockpiler-macOS.zip` - Contains `Stockpiler` executable and all required files  
- **Linux**: `Stockpiler-Linux.tar.gz` - Contains `Stockpiler` executable and all required files

### Files Included in Build

Each build includes:
- The main executable
- All CSV configuration files
- The application icon (`Bmat.ico`)
- `CheckImages/` directory with all image assets
- `UI/` directory with UI elements
- `Compare/` directory with comparison images
- Empty `Stockpiles/` directory for output

### Requirements

The workflow automatically:
- Installs Python 3.9
- Installs all dependencies from `requirements.txt`
- Installs PyInstaller
- Builds a single-file executable with `--onefile --windowed` flags

### Release Naming

Releases are automatically named with the format:
- Tag: `v{run_number}` (e.g., `v123`)
- Release name: `Stockpiler v{run_number}`

### Troubleshooting

If the build fails:
1. Check the Actions tab for error details
2. Ensure all dependencies in `requirements.txt` are correct
3. Verify that all required files exist in the repository
4. Check that the main Python file (`Stockpiler.py`) has no syntax errors

### Local Development

For local development, you can still use the existing build scripts:
- Windows: `build.bat` (uses Nuitka)
- Linux/macOS: `build.sh` (uses Nuitka)

The GitHub Actions workflow uses PyInstaller instead of Nuitka for consistency across platforms.

