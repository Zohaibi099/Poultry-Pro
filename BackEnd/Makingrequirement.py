import os

# Path to your 'site-packages' directory
site_packages_path = r"C:\Users\Zohaib\Desktop\Poultry Pro\env2\Lib\site-packages"

# List all the folders in 'site-packages'
packages = os.listdir(site_packages_path)

# Create a list to store package names and versions
requirements = []

for package in packages:
    # Check if the folder is a '.dist-info' folder (this is where version info is stored)
    if package.endswith('.dist-info'):
        # Extract package name and version
        package_name = package.split('-')[0]  # Extract package name before the first hyphen
        version = package.split('-')[1]  # Extract version after the first hyphen
        
        # Clean up the '.dist' suffix
        if version.endswith('.dist'):
            version = version.replace('.dist', '')

        # Format and append to the list
        requirements.append(f"{package_name}=={version}")

# Save the list to requirements.txt
with open("requirements.txt", "w") as f:
    for item in requirements:
        f.write(f"{item}\n")

print("requirements.txt file created successfully!")
#to install the packages use
# pip install -r requirements.txt
# to make requirements.txt
# echo freeze > requirements.txt