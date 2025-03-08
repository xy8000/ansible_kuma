#!/bin/sh

# usage:
#
# run all tests:
# ./run_tests.sh
#
# run all tests against specific uptime kuma version:
# ./run_tests.sh 1.19.4
#
# run all tests against specific uptime kuma version and specific modules:
# ./run_tests.sh 1.19.4 maintenance maintenance_info

function stop_kuma()
{
  echo "Stopping uptime kuma..."
  docker stop uptimekuma > /dev/null
}

venv_path="$HOME/git/ansible_kuma/venv/bin/python" #TODO: Change to generic path
collection_path="$HOME/.ansible/collections/ansible_collections/xy8000/uptime_kuma" #TODO: Change to generic path
initial_path=$(pwd)
version="$1"
modules="${@:2}"

echo "Using venv: $venv_path"
echo "Using collection-path: $collection_path"
echo "Initial path: $initial_path"

if [ ! -d "$collection_path" ]
then
  ansible-galaxy collection install git+https://github.com/xy8000/ansible_kuma.git
fi
cp -r ./{plugins,tests} "$collection_path"
cd "$collection_path"

if [ $version ] && [ "$version" != "all" ]
then
  versions=("$version")
else
  versions=(1.23.1 1.23.0 1.22.1 1.22.0 1.21.3)
fi

unit_targets=""
integration_targets=""
for module in ${modules[*]}
do
  unit_filepath="tests/unit/plugins/module_utils/test_${module}.py"
  unit_targets+="${unit_filepath} "

  integration_targets+="${module} "
done

for version in ${versions[*]}
do
  docker rm -f uptimekuma > /dev/null 2>&1

  echo "Starting uptime kuma $version..."
  docker run -d -it --rm -p 3001:3001 --name uptimekuma "louislam/uptime-kuma:$version" > /dev/null || exit 1

  while [[ "$(curl -s -L -o /dev/null -w ''%{http_code}'' 127.0.0.1:3001)" != "200" ]]
  do
    sleep 0.5
  done

  echo "Running unit tests..."
  ansible-test units -v --requirements --python-interpreter "$venv_path"  --num-workers 1 $unit_targets

  if [ $? != 0 ]; then
    echo "Error while executing unit-tests"
    stop_kuma
    break
  fi

  echo ""
  echo "Running integration tests..."
  ansible-test integration -v --requirements --python-interpreter "$venv_path" $integration_targets

  if [ $? != 0 ]; then
    echo "Error while executing unit-tests"
    stop_kuma
    break
  fi

  stop_kuma
  sleep 1

done

echo "Jumping back to initial path..."
cd $initial_path
echo "Done"