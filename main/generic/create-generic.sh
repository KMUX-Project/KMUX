#!/bin/bash
#
# KMUX - a free and open source small business server.
# Copyright (C) 2015, Julian Thomé <julian.thome.de@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

KMUXINST_VSERVER_NAME="{{name}}"
KMUXINST_VSERVER_PATH="var/lib/lxc"
KMUXINST_VSERVER_CHROOT_PATH="${{config['general']['vserver-path']}}/rootfs"
KMUXINST_VSERVER_ETC="{{config['general']['stage']}}"

KMUXINST_VSERVER_NR="{{nr}}"
KMUXINST_VSERVER_CONTEXT="10{{nr}}"

KMUXINST_VSERVER_PACKAGES="{{basepackages}}"

KMUXINST_VSERVER_DEBIAN_REPDIST_TMP={{dist}}

msg ${MSG_INFO} "Installing {{name}} VServer ..."

export KMUX_HANDLE_DAEMONS=${{config['general']['handle-daemons']}}

export DEBIAN_FRONTEND=noninteractive
export LANG=C

# Check if vserver already exists
if [ -d "${KMUXINST_VSERVER_CHROOT_PATH}/bin" -o -d "${KMUXINST_VSERVER_ETC}/context" -a ${KMUX_UPGRADE} = "false" ]
then
  msg ${MSG_WARN} "VServer ${KMUXINST_VSERVER_NAME} already exists."
  continue
fi

# Setting debian/ubuntu dist to etch
KMUXINST_DIST="debian"
KMUXINST_REPDIST="lenny"

if [ ${KMUXINST_DIST} = "debian" ]
then
  KMUXINST_REPSERVER=${KMUXINST_DEBIAN_REPSERVER}
  KMUXINST_REPSERVER_ARCH=${KMUXINST_DEBIAN_REPSERVER_ARCH}
  KMUXINST_SECURITY_REPSERVER=${KMUXINST_DEBIAN_SECURITY_REPSERVER}
else
  KMUXINST_REPSERVER=${KMUXINST_UBUNTU_REPSERVER}
  KMUXINST_REPSERVER_ARCH=${KMUXINST_UBUNTU_REPSERVER_ARCH}
  KMUXINST_SECURITY_REPSERVER=${KMUXINST_UBUNTU_SECURITY_REPSERVER}
fi

# Build zpub vserver base
if [ ${KMUX_UPGRADE} = "false" ]
then
  if [ ${INTERNAL_INSTALL} = "true" ]
  then
    lxc-create -n ${KMUXINST_VSERVER_NAME} -t ${KMUXINST_DIST} -f /etc/lxc/network.conf -- -r ${KMUXINST_REPDIST} --arch=i386 || msg ${MSG_ERR} "Unable to create Container ${KMUXINST_VSERVER_NAME}"
  else
    chroot ${KMUXINST_STAGE} lxc-create -n ${KMUXINST_VSERVER_NAME} -t ${KMUXINST_DIST} -f /etc/lxc/network.conf -- -r ${KMUXINST_REPDIST} --arch=i386 || msg ${MSG_ERR} "Unable to create Container ${KMUXINST_VSERVER_NAME}"
  fi
fi

# Mount proc
mount -t proc proc "{{config['vserver-path']}}/proc" || msg ${MSG_ERR} "Unable to mount ${KMUXINST_VSERVER_CHROOT_PATH}/proc"
# Mount dev
mount -o rbind /dev "${KMUXINST_VSERVER_CHROOT_PATH}/dev" || msg ${MSG_ERR} "Unable to mount ${KMUXINST_VSERVER_CHROOT_PATH}/dev"
# Mount sys
mount -t sysfs sys "${KMUXINST_VSERVER_CHROOT_PATH}/sys" || msg ${MSG_ERR} "Unable to mount ${KMUXINST_VSERVER_CHROOT_PATH}/sys"

# Create /etc/hosts
TMP_FILE="${KMUXINST_VSERVER_CHROOT_PATH}/etc/hosts"
{
  echo "127.0.0.1 localhost ${KMUXINST_VSERVER_NAME}"	> ${TMP_FILE};
} || msg ${MSG_ERR} "Unable to create ${TMP_FILE}"

# Set vserver hostname
if [ ${INTERNAL_INSTALL} = "false" -a ${KMUX_UPGRADE} = "false" ]
then
  chroot ${KMUXINST_VSERVER_CHROOT_PATH} hostname ${KMUXINST_VSERVER_NAME} || msg ${MSG_ERR} "Unable to set hostname"
fi

# Overwrite /etc/apt/sources.list
TMP_FILE="${KMUXINST_VSERVER_CHROOT_PATH}/etc/apt/sources.list"
if [ -e "${TMP_FILE}" -a ${KMUX_UPGRADE} = "true" ]; then cp "${TMP_FILE}" "${TMP_FILE}.backup"; fi # Backup the upgraded file
{
  echo "deb ${KMUXINST_DEBIAN_REPSERVER_ARCH} ${KMUXINST_REPDIST} main contrib non-free"     >  "${TMP_FILE}";
  echo "deb-src ${KMUXINST_DEBIAN_REPSERVER_ARCH} ${KMUXINST_REPDIST} main contrib non-free" >> "${TMP_FILE}";
  echo                                                                             >> "${TMP_FILE}";
  echo "deb ${KMUXINST_SECURITY_REPSERVER} ${KMUXINST_REPDIST}/updates main contrib non-free" >> "${TMP_FILE}";
  echo "deb-src ${KMUXINST_SECURITY_REPSERVER} ${KMUXINST_REPDIST}/updates main contrib non-free" >> "${TMP_FILE}";  
  echo                                                                             >> "${TMP_FILE}";
  if [ ${KMUX_DEBIAN_REPDIST} == "lenny" ]; then
     echo "deb ${KMUXINST_VOLATILE_REPSERVER} ${KMUXINST_REPDIST}/volatile main contrib non-free" >> "${TMP_FILE}";
     echo "deb-src ${KMUXINST_VOLATILE_REPSERVER} ${KMUXINST_REPDIST}/volatile main contrib non-free" >> "${TMP_FILE}";
     echo                                                                             >> "${TMP_FILE}";
  fi 
  echo "deb ${KMUXINST_KMUX_REPSERVER} ${KMUXINST_KMUX_REPDIST}"         >> "${TMP_FILE}";
  echo                                                                                         >> "${TMP_FILE}";
  echo "deb http://www.zpub.de/debian ./"          >> "${TMP_FILE}";
  echo                                                                                         >> "${TMP_FILE}";
} || msg ${MSG_ERR} "Unable to write to ${TMP_FILE}"

# Load debconf files
{
  echo "sun-java6-bin   shared/accepted-sun-dlj-v1-1    boolean true" | chroot ${KMUXINST_VSERVER_CHROOT_PATH} debconf-set-selections;
  echo "sun-java6-jdk   shared/accepted-sun-dlj-v1-1    boolean true" | chroot ${KMUXINST_VSERVER_CHROOT_PATH} debconf-set-selections;
  echo "sun-java6-jre   shared/accepted-sun-dlj-v1-1    boolean true" | chroot ${KMUXINST_VSERVER_CHROOT_PATH} debconf-set-selections;
} || msg ${MSG_ERR} "Error while setting debconf selections for sun-java5 and sun-java6."

# Set kernel install parameters
TMP_FILE="${KMUXINST_VSERVER_CHROOT_PATH}/etc/kernel-img.conf"
{
  echo "do_initrd = Yes"              >  "${TMP_FILE}";
  echo "clobber_modules = Yes"        >> "${TMP_FILE}";
  echo "link_in_boot = Yes"           >> "${TMP_FILE}";
} || msg ${MSG_ERR} "Unable to write to ${TMP_FILE}"

# Start-Stop daemon
chroot ${KMUXINST_VSERVER_CHROOT_PATH} dpkg-divert --add --rename --divert /sbin/start-stop-daemon.real /sbin/start-stop-daemon || msg ${MSG_ERR} "Error while changing the start-stop-daemon."

# Create new start-stop-daemon
TMP_FILE="${KMUXINST_VSERVER_CHROOT_PATH}/sbin/start-stop-daemon"
{
  echo "#!/bin/sh"														>  "${TMP_FILE}";
  echo "if [ \"\$KMUX_HANDLE_DAEMONS\" != \"false\" ]"       >> "${TMP_FILE}";
  echo "then"                                                                  >> "${TMP_FILE}";
  echo "/sbin/start-stop-daemon.real \"\$@\" "						>> "${TMP_FILE}";
  echo "fi"																		>> "${TMP_FILE}";
} || msg ${MSG_ERR} "Unable to write to ${TMP_FILE}"

# Change permissions
chmod 755 "${TMP_FILE}" || msg ${MSG_ERR} "Unable to change permissions on ${TMP_FILE}"

# Install policy-rc.d
TMP_FILE="${KMUXINST_VSERVER_CHROOT_PATH}/usr/sbin/policy-rc.d"
{
  echo "#!/bin/sh"														> "${TMP_FILE}";
  echo "[ \"\$KMUX_HANDLE_DAEMONS\" = \"false\" ] && exit 101 "	>> "${TMP_FILE}";
  echo "exit 0"																				>> "${TMP_FILE}";
} || msg ${MSG_ERR} "Unable to write to ${TMP_FILE}"

# Change permissions
chmod 755 "${TMP_FILE}" || msg ${MSG_ERR} "Unable to change permissions on ${TMP_FILE}"

# Set apt options
TMP_FILE="${KMUXINST_VSERVER_CHROOT_PATH}/etc/apt/apt.conf"
{
  echo "APT::Cache-Limit \"100000000\";"	> "${TMP_FILE}";
  echo "APT::Default-Release \"${KMUXINST_REPDIST}\";"	>> "${TMP_FILE}";
  echo "APT::Get::AllowUnauthenticated \"true\";" >> "${TMP_FILE}";
} || msg ${MSG_ERR} "Unable to write to ${TMP_FILE}"

rm "${KMUXINST_VSERVER_CHROOT_PATH}/etc/resolv.conf"
cp "/etc/resolv.conf" "${KMUXINST_VSERVER_CHROOT_PATH}/etc" || msg ${MSG_ERR} "Unable to copy resolv.conf from install-host system"

# Install and create locales
chroot ${KMUXINST_VSERVER_CHROOT_PATH} apt-get update || msg ${MSG_WARN} "Warning incomplete update of package list."
chroot ${KMUXINST_VSERVER_CHROOT_PATH} apt-get -y install locales || msg ${MSG_ERR} "Unable to install locales."

TMP_FILE="${KMUXINST_VSERVER_CHROOT_PATH}/etc/locale.gen"
{
  echo "${KMUXINST_LOCALE}.UTF-8 UTF-8" > "${TMP_FILE}";
  echo "${KMUXINST_LOCALE} ISO-8859-1" >> "${TMP_FILE}";
  echo "${KMUXINST_LOCALE}@euro ISO-8859-15" >> "${TMP_FILE}";
} || msg ${MSG_ERR} "Unable to write ${TMP_FILE}"
  
{
  chroot ${KMUXINST_VSERVER_CHROOT_PATH} locale-gen;
  chroot ${KMUXINST_VSERVER_CHROOT_PATH} update-locale LANG=${KMUXINST_LOCALE}.UTF-8;
} || msg ${MSG_ERR} "Unable to generate and update locales."

# Install packages with chroot
if [ ! -z "${KMUXINST_VSERVER_PACKAGES}" ]
then
  chroot ${KMUXINST_VSERVER_CHROOT_PATH} apt-get -y --force-yes install kmux-keyring || msg ${MSG_ERR} "Unable to install KMUX installation key-ring."
  chroot ${KMUXINST_VSERVER_CHROOT_PATH} apt-get update
  chroot ${KMUXINST_VSERVER_CHROOT_PATH} apt-get -y install ${KMUXINST_VSERVER_PACKAGES} || msg ${MSG_ERR} "Unable to install ${KMUXINST_VSERVER_PACKAGES}."
fi

# Install monit
./ebuilds-enabled/20-kmux-ebuild-monit -i ${KMUXINST_VSERVER_CHROOT_PATH} || msg ${MSG_ERR} "monit ebuild not enabled or installation failed."

# Reset Debian dist
KMUXINST_DEBIAN_REPDIST=${KMUXINST_VSERVER_DEBIAN_REPDIST_TMP}

# Unmount proc
umount -l "${KMUXINST_VSERVER_CHROOT_PATH}/proc" || msg ${MSG_ERR} "Unable to unmount ${KMUXINST_VSERVER_CHROOT_PATH}/proc"
# Unmount dev
umount -l "${KMUXINST_VSERVER_CHROOT_PATH}/dev" || msg ${MSG_ERR} "Unable to unmount ${KMUXINST_VSERVER_CHROOT_PATH}/dev"
# Unmount sys
umount -l "${KMUXINST_VSERVER_CHROOT_PATH}/sys" || msg ${MSG_ERR} "Unable to unmount ${KMUXINST_VSERVER_CHROOT_PATH}/sys"


# data-lvm: 
# sync data and mount directory
DATA_DIR=${KMUXINST_STAGE}/data
if [ -d $DATA_DIR ]; then
   # data-directories and mount-points
   VSERVER_DATA_DIR=${KMUXINST_VSERVER_CHROOT_PATH}/opt
   LVM_DATA_DIR=${DATA_DIR}/${KMUXINST_VSERVER_NAME}/opt
   mkdir -p ${LVM_DATA_DIR}
   rsync -a $VSERVER_DATA_DIR/ $LVM_DATA_DIR/
   echo "$VSERVER_DATA_DIR synced" 
   mount -o bind $LVM_DATA_DIR $VSERVER_DATA_DIR
   echo "$LVM_DATA_DIR mounted" 
fi

ln -s /${KMUXINST_VSERVER_PATH}/${KMUXINST_VSERVER_NAME}/config ${KMUXINST_STAGE}/etc/lxc/auto/${KMUXINST_VSERVER_NAME}

msg ${MSG_OK} "Successfully installed {{name}} VServer."

