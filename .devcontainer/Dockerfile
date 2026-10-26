FROM mcr.microsoft.com/devcontainers/typescript-node:24-bookworm

# Linux sandbox prerequisites for the Copilot Agent Host. Keep these in the
# image so Codespace rebuilds do not lose network/network-filtering support.
RUN apt-get update \
	&& DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		bubblewrap \
		iptables \
		slirp4netns \
		util-linux \
	&& rm -rf /var/lib/apt/lists/*

# GitKraken MCP is used by the remote Agent Host; pin the installer version.
RUN npm install -g --allow-scripts=@gitkraken/gk @gitkraken/gk@3.1.77

ADD install-vscode.sh /root/
RUN /root/install-vscode.sh

RUN git config --system codespaces-theme.hide-status 1

USER node
RUN npm install -g node-gyp
RUN NPM_CACHE="$(npm config get cache)" && rm -rf "$NPM_CACHE" && ln -s /vscode-dev/npm-cache "$NPM_CACHE"
RUN echo 'export DISPLAY="${DISPLAY:-:1}"' | tee -a ~/.bashrc >> ~/.zshrc

USER root
CMD chown node:node /vscode-dev && sudo -u node mkdir -p /vscode-dev/npm-cache && sleep inf
