# Hello, CloudLab

In this tutorial, you will learn how to use CloudLab to run experiments in computer networks or cloud computing.

CloudLab is a "virtual lab" for experiments on networking, cloud computing, and distributed systems. It allows experimenters to set up real (not simulated!) end hosts and links at one or more CloudLab host sites located around the United States. Experimenters can then log in to the hosts asociated with their experiment and install software, run applications to generate traffic, and take network measurements.

Before you can run lab experiments on CloudLab, you will need to set up an account. Once you have completed the steps on this page, you will have an account that you can use for future experiments.

## Prepare your workstation

You'll need to prepare your workstation (the laptop or PC you are going to use for your experiments0 with all necessary software. You will need two pieces of software:

* An appropriate terminal application
* Wireshark


### Terminal software

To use CloudLab, the primary software application you'll need is a terminal, which you will use to log in to remote hosts over SSH and carry out various exercises.

You may have a terminal application already on your workstation, but it may not be ideal for this purpose. When you run experiments on remote hosts, you will often have to run and monitor the output of multiple commands in several independent terminal sessions. It is therefore recommended to use a terminal that lets you split one terminal window into multiple panes - for example,

* [cmder](https://cmder.net/) for Windows. (Get the full version, not the mini version.)
* [iTerm2](https://www.iterm2.com/) for Mac
* [terminator](https://launchpad.net/terminator) for Linux

Once you have downloaded and installed your terminal application, open it up and practice using it. Make sure you know:

* How to split the pane in your terminal. 
* How to copy text from your terminal and paste into another application. This will be helpful when you need to save some terminal output for your lab report.
* How to copy text from another application and paste into your terminal. This will be helpful when you need to copy a command from the lab instructions into your terminal, in order to run it.

#### cmder on Windows

If you are using cmder on Windows, you can split the pane as follows:

1. Click on the green + symbol near the bottom right side of the window. This will open a "Create new console" dialog.
2. Where it says "New console split", choose "to bottom" or "to right". You can leave other options at their default settings.
3. Click "Start".

Note that if you need to split more than once, click on the pane that you want to split (so that it is the active pane) before using the green + symbol to split it again. 

To copy text from the terminal, select the text you want to copy. It will be automatically copied to your clipboard, and you can then paste it into any other application.

To paste text into the terminal, place your cursor where you want to paste, and right click.


#### iTerm2 on Mac

If you are using iTerm2 on Mac, you can split the pane as follows:

1. To create a new vertical pane, use ⌘+D
2. To create a new horizontal pane, use ⌘+Shift+D

To copy text from the terminal, select the text you want to copy and use ⌘+C to copy.

To paste text into the terminal, place your cursor where you want to paste, and use ⌘+V to paste.

#### Terminator on Linux

If you are using `terminator` on Linux, you can split the pane either vertically or horizontally as follows:

1. Right-click anywhere inside the terminal window
2. Choose "Split pane horizontally" or "Split pane vertically"
3. You can resize panes by dragging the divider between panes

To copy text from the terminal, select the text you want to copy and either

* right-click, and choose Copy, or
* use Ctrl+shift+C to copy

To paste text into the terminal, place your cursor where you want to paste, and either

* right-click, and choose Paste, or
* use Ctrl+shift+P to paste

### Wireshark

Wireshark is a software application for capturing, viewing, and analyzing network packets. Download Wireshark from [the Wireshark website](https://www.wireshark.org/download.html).

Then, follow the instructions to install for your system:

* [Instructions for installing Wireshark on Windows](https://www.wireshark.org/docs/wsug_html_chunked/ChBuildInstallWinInstall.html). (Note: you only need Wireshark, not the extra components that are bundled along with it.)
* [Instructions for installing Wireshark on Mac](https://www.wireshark.org/docs/wsug_html_chunked/ChBuildInstallOSXInstall.html).
* [Instructions for installing Wireshark on Linux](https://www.wireshark.org/docs/wsug_html_chunked/ChBuildInstallUnixInstallBins.html).


## Set up your account on CloudLab

Now that you have the software you need, you are ready to set up an account on CloudLab.

### Exercise - Set up SSH keys

In this exercise, you will set up a pair of SSH keys with which you will access resources on CloudLab. (If you have previously used SSH keys, and have a public and private key ready to use, you can skip to the next exercise.)

CloudLab users access resources using *public key authentication*. Using SSH public-key authentication to connect to a remote system is a more secure alternative to logging in with an account password.

SSH public-key authentication uses a pair of separate keys (i.e., a key pair): one "private" key, which you keep a secret, and the other "public". A key pair has a special property: any message that is encrypted with your private key can only be decrypted with your public key, and any message that is encrypted with your public key can only be decrypted with your private key.

This property can be exploited for authenticating login to a remote machine. First, you upload the public key to a special location on the remote machine. Then, when you want to log in to the machine:

1. You use a special argument with your SSH command to let your SSH application know that you are going to use a key, and the location of your private key. If the private key is protected by a passphrase, you may be prompted to enter the passphrase (this is not a password for the remote machine, though.)
2. The machine you are logging in to will ask your SSH client to "prove" that it owns the (secret) private key that matches an authorized public key. To do this, the machine will send a random message to you.
3. Your SSH client will encrypt the random message with the private key and send it back to the remote machine.
5. The remote machine will decrypt the message with your public key. If the decrypted message matches the message it sent you, it has "proof" that you are in possession of the private key for that key pair, and will grant you access (without using an account password on the remote machine.)

(Of course, this relies on you keeping your private key a secret.)

On your laptop, you're going to generate a key pair and upload the public key to the CloudLab portal. Then, you'll use that key from now on to log in to CloudLab resources. Open a Bash terminal (such as `cmder` in Windows, or the built-in terminal in Mac or Linux).

Generate a key with:

```
ssh-keygen -t rsa
```

and follow the prompts to generate and save the key pair. The output should look something like this:

```
$ ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/users/ffund01/.ssh/id_rsa): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /users/ffund01/.ssh/id_rsa.
Your public key has been saved in /users/ffund01/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:z1W/psy05g1kyOTL37HzYimECvOtzYdtZcK+8jEGirA ffund01@example.com
The key's randomart image is:
+---[RSA 2048]----+
|                 |
|                 |
|           .  .  |
|          + .. . |
|    .   S .*.o  .|
|     oo. +ooB o .|
|    E .+.ooB+* = |
|        oo+.@+@.o|
|        ..o==@ =+|
+----[SHA256]-----+
```

In a safe place, make a note of:

* The passphrase you used,
* The full path to your private key (`/users/ffund01/.ssh/id_rsa` in the example above) - copy and paste this from your terminal output,
* The full path to your public key, which has the same name as your private key but with a `.pub` extension (`/users/ffund01/.ssh/id_rsa.pub` in the example above) - copy and paste this from your terminal output.

If you forget these, you won't be able to access resources on CloudLab from your terminal - so hold on to this information!

### Exercise - Create an account

> Note
> To complete this step, you'll need to know the **Project Name** of the project that you will join. Your instructor or research advisor will tell you the project name to use.


First, go to [https://cloudlab.us](https://cloudlab.us) and click on "Request an Account".  You will see a form, like this one:

![Creating an account and joining a project on CloudLab.](images/join-project.png)

You will fill in 

* your desired username (by convention, this should be lowercase, and have no spaces or special characters), 
* your full name, school email address, and country, state, and city. 
* For "Institutional Affiliation", you will use the name of your college or university (your instructor may specify the exact text you should use).

Click on the "Choose File" button in the *SSH Public Key file* section, and upload your public key from the previous step. Your public key is the one with the `.pub` file extension.

> **Note**: If you are having trouble uploading your public key to the portal because you aren't able to find it in the file browser, you can copy it to a more convenient location and upload it from there.
>
> * Open a terminal.
> * Run `cp /path/to/key.pub /path/to/new/location` but substituting the path to your key and the path to a more convenient location (e.g. your Desktop) for the two arguments.
> * Upload the public key from the new location.
> * You can delete the copy of the public key from the new location (the original key is still located at the original location).


In the "Password" field, enter the password you want to use to log in to the CloudLab web portal. Then, in the "Confirm Password" field, enter the same password again.

In the Project Information section, select "Join Existing Project". Then, in the "Project Name" field, enter the project name that your instructor or research advisor gave you.


### Exercise - View or edit keys on CloudLab

Next, upload your public key to the SSH Keys section of your profile on the GENI CloudLab: in the menu, click on your name, then on "[SSH Keys](https://portal.geni.net/secure/profile.php#ssh)", and upload your public key to that page. Your public key is the one with the `.pub` file extension.


> **Note**: If you are having trouble uploading your public key to the portal because you aren't able to find it in the file browser, you can copy it to a more convenient location and upload it from there.
>
> * Open a terminal.
> * Run `cp /path/to/key.pub /path/to/new/location` but substituting the path to your key and the path to a more convenient location (e.g. your Desktop) for the two arguments.
> * Upload the public key from the new location.
> * You can delete the copy of the public key from the new location (the original key is still located at the original location).


Once your key is in the portal, every time you reserve GENI resources, your key will automatically be placed in the "authorized keys" list so that you can access the resource. 

Note that this only applies to resources you reserved after uploading a key. If you lose access to your key and have to generate and upload a new key, you will lose the ability to log on to resources you have reserved in the past.

In general, a common mistake students make is to delete or replace their keys if they are having trouble logging in to a resource. This is usually not helpful, and in most cases makes things worse. Deleting a key is like forgetting a password - don't do it!

---

<small>Questions about this material? Contact Fraida Fund</small>

---

<small>This material is based upon work supported by the National Science Foundation under Grant No. 2231984.</small>
<small>Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.</small>