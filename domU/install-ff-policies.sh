#!/bin/sh

function install_ff_policies() {
  local target=`hostname`;
  local source="/etc/firefox/policies/${target}.json";
  local pol_file="/usr/lib64/firefox/distribution/policies.json";

  ! [[ `whoami` == "root" ]] && echo "must be run as root" && return 3;
  [[ -z $target ]] && echo "error: must set target" && return 1;
  ! [[ -f $source ]] && echo "error: target policy '${target}' doesn't exist" && return 2;

  cat $source > $pol_file;

  local status=$?;
  [[ $status == 0 ]] && echo "policies installed" || echo "error: policies not installed";

  return $status;
}

install_ff_policies $@
unset install_ff_policies
