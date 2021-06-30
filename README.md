# Domain Skeleton using WHM/cPanel Hooks

Since cPanel doesn't seem to want to have a [skeleton directory for subdomains and addons](https://features.cpanel.net/topic/skeleton-directory-for-addon-and-sub-domains), we decided to use [cPanel/WHM Standardized Hooks](https://documentation.cpanel.net/display/DD/Guide+to+Standardized+Hooks) to accomplish the same thing.

This uses the [`Cpanel` category of hookable events](https://documentation.cpanel.net/display/DD/Guide+to+Standardized+Hooks+-+Cpanel+Functions). Specifically, the  [AddonDomain::addaddondomain (API2)](https://documentation.cpanel.net/display/DD/cPanel+API+2+Functions+-+AddonDomain%3A%3Aaddaddondomain) and [SubDomain::addsubdomain (UAPI)](https://documentation.cpanel.net/display/DD/UAPI+Functions+-+SubDomain%3A%3Aaddsubdomain) endpoints.

## Installation/Setup

Perform the following steps on your cPanel server as `root`.

1. Clone this repo where you plan to keep your hooks (`/usr/local/cpanel/3rdparty/bin/` seems to be where they want it, but [some documents](https://documentation.cpanel.net/display/DD/Guide+to+Standardized+Hooks+-+The+describe%28%29+Method) seem to point elsewhere).
2. Change permissions to 0755 (`chmod 0755 domain_skel.py`).
3. Create a Python virtual environment for executing your script (`python -m venv <venv dir>`) -- it can be in the same directory where you cloned this repo.
4. Source your virtual environment (`source <venv dir>/bin/activate`).
5. `cd` to the repo directory and install the requirements (`pip install -r requirements.txt`).
6. Create a directory where you want to keep your skeleton files (we used `/root/keobi-domain-skel`) and upload any files.
7. Update the `config.py` file -- specifically `PROJECT_NAME`, `LOG_FILE`, `HOOK_SCRIPT_DIR`, `PYTHON_EXE`, and `DOMAIN_SKEL_SKELDIR`.
8. Update the [shebang (#!)](https://en.wikipedia.org/wiki/Shebang_(Unix)) line in the `domain_skel.py` to `<ven dir>/bin/python`.
9. Register the hook: `/usr/local/cpanel/bin/manage_hooks add script <HOOK_SCRIPT_DIR>/domain_skel.py`
10. Verify the hooks in WHM by logging into WHM and clicking "Manage Hooks" under "Development".

You should be done! Test it out by creating an addon or subdomain.

## Troubleshooting

You can somewhat test the script using the [`hook` script](https://docs.cpanel.net/whm/scripts/the-hook-script/):
* `/usr/local/cpanel/scripts/hook --category Cpanel --event Api2::AddonDomain::addaddondomain --stage=post`
* `/usr/local/cpanel/scripts/hook --category Cpanel --event UAPI::SubDomain::addsubdomain --stage=post`

You can also enable Hook Debugging in WHM:
Server Configuration > Tweak Settings > Development > Standardized Hooks - Debug > "Debug mode is on. The system displays information about a hook while it executes and logs debug data to the error log.".

### Log Files

Primary logging output will be to the `LOG_FILE` file you setup in `config.py`

If Hook Debugging is enabled (see above), you can use the cPanel error log: `/usr/local/cpanel/logs/error_log`
