# Mac Signing and Notarization Demo

### ❓ How to sign and notarize an Electron App for macOS?

**1. Initial Setup**
1. Create an Apple Account if you don't have one.
2. Install Xcode and Apple Developer App from the App Store.
3. Open the Apple Developer App and subscribe to the $99 Apple Developer Program, providing accurate details as per your *National ID*.
4. Wait until you receive the Apple Developer Program Welcome Email, which may take up to 48 hours.

**2. Get Required Credentials**

*App Specific Password:*
1. Visit https://account.apple.com/account/manage.
2. Sign in to your Apple Account.
3. Create a new App Specific Password and store it securely.

*Developer ID Application Certificate:*
1. Open Xcode > Settings > Account > "Manage Certificates".
2. Click "+" to create a "Developer ID Application Certificate".
3. Generate a random password at https://www.avast.com/en-in/random-password-generator.
4. Left-click the Certificate, export it:
   - Use the generated password.
   - Name the file "certificate".
   - Save "certificate.p12" in a secure location.

*Team ID:*
1. Visit https://developer.apple.com/account.
2. Scroll to the "Membership details" Card and copy the "Team ID" to a secure place.

**3. Sign and Notarize Sample Application**

*Important Notes:*
- Perform this at night, as the first-time notarization can take 8 to 12 hours (subsequent notarizations are done in 10 minutes).
- Sign and notarize the provided sample app to understand the process. You can later follow the steps in the next section to sign and notarize your own application.

*Steps:*
1. Set up the sample app:
```
git clone https://github.com/omkarcloud/macos-code-signing-example
cd macos-code-signing-example
npm install
```
2. Ensure you have the latest version of Electron Builder installed to avoid any errors:

```
npm install --save-dev electron-builder@latest
```
3. Place the "certificate.p12" file exported earlier in the root directory.
4. Create a "package-mac-signed.sh" file, paste the following content, and then replace placeholders with your credentials:
```bash
export APPLE_ID="username@gmail.com" # Replace with your Apple ID email
export APPLE_APP_SPECIFIC_PASSWORD="MY_APP_SPECIFIC_PASSWORD" # Replace with your App Specific Password, it looks like "dsjg-zqet-rpzp-nfzy"
export APPLE_TEAM_ID="MY_TEAM_ID" # Replace with your Team ID, it looks like "AB8Y7TRS2P"
export CSC_LINK="./certificate.p12" # Keep it as it is
export CSC_KEY_PASSWORD="MY_CERTIFICATE_PASSWORD" # Replace with your Certificate Password
npm run package
```
5. Run `bash package-mac-signed.sh`.
6. Once you see the "notarization successful" message in the terminal, you can now distribute the ".dmg" via the internet to your users without facing any security warnings. Hurray! 🎉
7. Now, let's proceed to sign and notarize your own custom application using Electron Builder.

**4. Signing Your Own Application**

1. Ensure you have the latest version of Electron Builder installed to avoid any errors:

```
npm install --save-dev electron-builder@latest
```
2. Ensure your "entitlements.mac.plist" has the following entitlements for Electron to function:
```xml
<key>com.apple.security.cs.allow-jit</key>
<true/>
<key>com.apple.security.cs.allow-unsigned-executable-memory</key>
<true/>
```
3. Ensure that in your "package.json", the Electron "build" config's "mac" section looks like the following for creating a universal build. Using a universal build for installation will avoid confusion among Intel and M-series Mac users:
```json
{
  "mac": {
    "category": "public.app-category.developer-tools",
    "target": [
      {
        "target": "default",
        "arch": ["universal"]
      }
    ],
    "artifactName": "${productName}.${ext}",
    "type": "distribution",
    "hardenedRuntime": true,
    "entitlements": "assets/entitlements.mac.plist",
    "entitlementsInherit": "assets/entitlements.mac.plist",
    "gatekeeperAssess": false
  }
}
```

4. In your package.json scripts, ensure there is a script to build the Mac DMG:
```json
{
  "scripts": {
   "package": "ANY_PRE_BUILD_STEPS && electron-builder build --publish never && ANY_POST_BUILD_STEPS",
  }
}
```
Also, add the following script, which will help you create an unsigned build, which is useful for testing:
```json 
{
  "scripts": {
  "package:mac-unsigned": "ANY_PRE_BUILD_STEPS && electron-builder build -c.mac.identity=null --publish never && ANY_POST_BUILD_STEPS",
  }
}
```
Replace ANY_PRE_BUILD_STEPS and ANY_POST_BUILD_STEPS with your pre and post-build steps, if you have any. If you don't have any, remove them.
5. Optionally, in your package.json file, change the following properties, as they are shown in several places on the OS UI to the end user:
   - `name`
   - `description`
   - `build.productName`
   - `appId`
     The `appId` is the reverse of your (website name) + (product name in Title Case).
     For example, if your website is "awesome-app.com" and your product name is "Awesomeness", then your `appId` will be "com.awesome-app.Awesomeness".
```json
{
    "name": "your-app-name",
    "description": "Your app description",
    "build": {
        "productName": "Your App Name",
        "appId": "com.awesome-app.Awesomeness"
    }
}
```
If you are using boilerplates like "electron-react-boilerplate", you will also need to change the "release/app/package.json" file with:
   - `name`: Same as the main package.json
   - `version`
   - `description`: Same as the main package.json
```json
{
    "name": "your-app-name",
    "version": "1.0.0",
    "description": "Your app description"
}
```
Here's an example Electron Builder configuration that follows best practices for creating an Electron app on macOS, Windows, and Linux:

```json
{
  "build": {
    "productName": "Awesomeness",
    "appId": "com.awesome-app.Awesomeness",

    "mac": {
      "category": "public.app-category.developer-tools",
      "target": [
        {
          "target": "default",
          "arch": [
            "universal"
          ]
        }
      ],
      "artifactName": "${productName}.${ext}",
      "type": "distribution",
      "hardenedRuntime": true,
      "entitlements": "assets/entitlements.mac.plist",
      "entitlementsInherit": "assets/entitlements.mac.plist",
      "gatekeeperAssess": false
    },
    "dmg": {
      "contents": [
        {
          "x": 130,
          "y": 220
        },
        {
          "x": 410,
          "y": 220,
          "type": "link",
          "path": "/Applications"
        }
      ]
    },
    "win": {
      "target": [
        "nsis"
      ],
      "artifactName": "${productName}.${ext}"
    },
    "linux": {
      "artifactName": "${productName}-${arch}.${ext}",
      "target": [
        {
          "target": "deb",
          "arch": [
            "arm64",
            "x64"
          ]
        },
        {
          "target": "rpm",
          "arch": [
            "arm64",
            "x64"
          ]
        }
      ],
      "category": "Development"
    }
    // Rest of Electron Builder config
  }
}
```    


6. Create a "package-mac-signed.sh" file, paste the following content, and then replace placeholders with your credentials:
```sh
export APPLE_ID="username@gmail.com" # Replace with your Apple ID email
export APPLE_APP_SPECIFIC_PASSWORD="MY_APP_SPECIFIC_PASSWORD" # Replace with your App Specific Password, it looks like "dsjg-zqet-rpzp-nfzy"
export APPLE_TEAM_ID="MY_TEAM_ID" # Replace with your Team ID, it looks like "AB8Y7TRS2P"
export CSC_LINK="./certificate.p12" # Keep it as it is
export CSC_KEY_PASSWORD="MY_CERTIFICATE_PASSWORD" # Replace with your Certificate Password
npm run package
```
7. Place the "certificate.p12" file exported earlier in the root directory.
8. Add the "certificate.p12" and "package-mac-signed.sh" to the .gitignore file, as these contain sensitive information that should not be shared in your GitHub repository.
```
package-mac-signed.sh
certificate.p12
```
9. Run `bash package-mac-signed.sh`.
10. Wait until you see the "notarization successful" message in the terminal - your app is ready for the world to see! Congratulations! 🎉

### ❓ How to automate the above process using GitHub Actions?

**1. GitHub Repository Setup**
1. Create a new repository.
2. Push your code.
3. Encode the certificate and save the output in a secure place:
```bash
base64 -i certificate.p12
```

**2. Create S3 Bucket**
1. Open AWS Console > S3.
2. Click "Create bucket".
3. Configure the bucket:
```
Bucket name: Enter a unique bucket name in kebab case (e.g., my-app-name-distribution)
Block Public Access settings for this bucket: Uncheck "Block all public access"
```
4. Click on "Create bucket".
5. Go to the bucket.
6. Enable public access:
   - Go to the "Permissions" tab.
   - In the "Bucket policy" section, press the "Edit" button and paste the following policy (replace "<bucket-name>" with the bucket name you just created):
```json
{
    "Version": "2008-10-17",
    "Statement": [
        {
            "Sid": "AllowPublicRead",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::<bucket-name>/*"
        }
    ]
}
```
If you don't have them, then get AWS access key and secret key.

**3. Configure GitHub Secrets**
In your GitHub Repository, navigate to Settings > Secrets and variables > Actions and add the following secrets:
```
APPLE_ID                     # Your Apple ID email
APPLE_APP_SPECIFIC_PASSWORD  # App Specific password
APPLE_TEAM_ID                # Your Team ID
CSC_BASE64_ENCODED           # Your Base64 encoded certificate created earlier
CSC_KEY_PASSWORD             # Certificate password
AWS_ACCESS_KEY_ID            # AWS access key
AWS_SECRET_ACCESS_KEY        # AWS secret key
```

**4. Set up GitHub Actions**
Create a `.github/workflows/package.yaml` file with the following contents:
```yaml
name: Package

on: [push, pull_request]

jobs:
  package-mac:
    # Notarization is taking too long, exit
    timeout-minutes: 30
    runs-on: macos-latest
    steps:
      - name: Check out Git repository
        uses: actions/checkout@v3

      - name: Install Node.js and NPM
        uses: actions/setup-node@v3
        with:
          node-version: 20
          cache: npm
 
      - name: Recreate certificate.p12 from Base64
        run: echo "${{ secrets.CSC_BASE64_ENCODED }}" | base64 -d > certificate.p12

      - name: npm install
        run: |
          npm install

      - name: Package
        env:
          APPLE_ID: ${{ secrets.APPLE_ID }}
          APPLE_APP_SPECIFIC_PASSWORD: ${{ secrets.APPLE_APP_SPECIFIC_PASSWORD }}
          APPLE_TEAM_ID: ${{ secrets.APPLE_TEAM_ID }}
          CSC_LINK: ./certificate.p12
          CSC_KEY_PASSWORD: ${{ secrets.CSC_KEY_PASSWORD }}
        run: |
          npm run package

      - name: Install packages needed for S3 upload
        run: |
          python -m pip install botasaurus boto3

      - name: Upload to S3
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}        
        run: |
          python .erb/scripts/upload-to-s3.py

  package-windows:
    timeout-minutes: 30
    runs-on: windows-latest

    steps:
      - name: Check out Git repository
        uses: actions/checkout@v3

      - name: Install Node.js and NPM
        uses: actions/setup-node@v3
        with:
          node-version: 20
          cache: npm

      - name: npm install
        run: |
          npm install

      - name: Package
        run: |
          npm run package

      - name: Install botasaurus package
        run: |
          python -m pip install botasaurus boto3

      - name: Upload to S3
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}        
        run: |
          python .erb/scripts/upload-to-s3.py

  package-linux:
    timeout-minutes: 30
    runs-on: ubuntu-latest

    steps:
      - name: Check out Git repository
        uses: actions/checkout@v3

      - name: Install Node.js and NPM
        uses: actions/setup-node@v3
        with:
          node-version: 20
          cache: npm

      - name: npm install
        run: |
          npm install

      - name: Package
        run: |
          npm run package

      - name: Install packages needed for S3 upload
        run: |
          python -m pip install botasaurus boto3

      - name: Upload to S3
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}        
        run: |
          python .erb/scripts/upload-to-s3.py                  
```

**5. Create Upload Script**
Create a `scripts/upload-to-s3.py` file with the following content. Replace "MY_BUCKET_NAME" with your bucket name:
```python
from botasaurus import bt
from botasaurus.env import get_os
from botasaurus.task import task
import os

bucket_name = "MY_BUCKET_NAME"

@task(output=None, raise_exception=True, close_on_crash=True, parallel=4)
def upload(data):
    upload_file_name = bt.trim_and_collapse_spaces(os.path.basename(data)).replace(' ','')
    
    uploaded_file_url = bt.upload_to_s3(
        data,
        bucket_name,
        os.environ['AWS_ACCESS_KEY_ID'],
        os.environ['AWS_SECRET_ACCESS_KEY'],
        upload_file_name,
    )
    
    print(f"Visit {uploaded_file_url} to download the uploaded file.") # URL to share with users

app_name = bt.read_json('./package.json')['build']['productName']
operating_system = get_os()

if operating_system == "mac":
    upload(f"./release/build/{app_name}.dmg")
elif operating_system == "windows":
    upload(f"./release/build/{app_name}.exe")
elif operating_system == "linux":
    upload(
        [
            f"./release/build/{app_name}-amd64.deb",
            f"./release/build/{app_name}-arm64.deb",
            f"./release/build/{app_name}-x86_64.rpm",
            f"./release/build/{app_name}-aarch64.rpm",
        ]
    )
```

**6. Deploy**
1. Push the code to GitHub.
2. Go to the Repository "Actions" tab to see the build process in action.
3. Once successfully completed, the URL to the uploaded file will be displayed in the logs of the "Upload to S3" section.
4. Share the URL with your users to distribute the signed and notarized executable. Hurray! 🎉
