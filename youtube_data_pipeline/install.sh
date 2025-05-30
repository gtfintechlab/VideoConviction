if conda env list | grep -q "youtube_data_pipeline_env"; then
  conda env remove -n youtube_data_pipeline_env
fi

if ! conda env list | grep "youtube_data_pipeline_env"; then
  conda env create -f environment.yaml
fi

source $(conda info --base)/etc/profile.d/conda.sh

conda activate youtube_data_pipeline_env

# Check if .env file already exists, if not, create it
if [ ! -f .env ]; then
  cat <<EOL > .env
YOUTUBE_API_KEY=""
EOL
else
  echo ".env file already exists, skipping creation."
fi