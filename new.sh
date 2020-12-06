#!/bin/bash
# @Description: Innit: Create new project scaffolding.


ASSETS='assets'
BUILD='build'
CONFIG='config'
DOCKER='docker'
HELM='helm'
LIB='lib'
TESTS='tests'

DIR_PATH=${HOME}'/'


function show_usage (){
  printf "Usage: $0 [options [parameters]]\n"
  printf "\n"
  printf "Options:\n"
  printf " -n|--name [name], Project name, which will be its directory name.  \n"
  printf " -p|--path [name], Project directory path, defaults to home (~)  \n"
  printf " -g|--git, Initialise as new git projct. (default is no.) \n"
  printf " -v|--verbose, Announce every little thing. \n"
  printf " -h|--help, Print help\n"
return 0
}
if [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]];then
  show_usage
fi

# This can be consolidated with the actual invocation.
function get_project_name (){

  if [[ ${1:0:1} == "-" ]] ; then
    echo "Sorry, project name cannot begin with a dash" ; exit 1;
  else
    PROJ=$1
    echo "Project name has been set to:  $1"
    shift
  fi
  return 0
}

function get_dir_path (){

  if [[ ${1:0:1} == "-" ]] ; then
    echo "Sorry, project directory cannot begin with a dash" ; exit 1;
  else
    DIR_PATH=$1
    echo "Project directory has been set to:  $1"
    shift
  fi
  return 0
}

while [ ! -z "$1" ]; do
  case "$1" in
     --name|-n)
      shift
      get_project_name "$@"
      ;;
    --path|-p)
     shift
     get_dir_path "$@"
     ;;
   --git|-g)
    GIT=y
    echo "Initializing Git repo after scaffolding project."
    shift
    ;;
   *)
    show_usage
    ;;
  esac
shift
done

if [[ -z "$PROJ" ]]; then
  echo "Sorry, can't continue. What's the project name?" ; exit 1;
fi

PROJ_PATH=${DIR_PATH}${PROJ}

mkdir -p ${PROJ_PATH}
mkdir -p $PROJ_PATH/$ASSETS
mkdir -p $PROJ_PATH/$CONFIG
mkdir -p $PROJ_PATH/$DOCKER
mkdir -p $PROJ_PATH/$HELM
mkdir -p $PROJ_PATH/$TESTS
mkdir -p $PROJ_PATH/$LIB
mkdir -p $PROJ_PATH/$LIB/c
mkdir -p $PROJ_PATH/$LIB/ext

cp -r files/gitignore $PROJ_PATH/.gitignore
cp -r files/build $PROJ_PATH
cp -r files/common $PROJ_PATH
cp -r files/LICENSE.md $PROJ_PATH

# @TODO: Check Git is locally installed, etc.
if [[ ! -z "$GIT" ]]; then
  git init
  #touch config/.keep
  #touch docker/.keep
  #touch helm/.keep
  touch lib/c/.keep
  touch lib/ext/.keep
fi
