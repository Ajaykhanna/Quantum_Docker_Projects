FROM python:3.7

WORKDIR /app
ADD . .

RUN pip install argparse==1.4.0 numpy==1.18.4 matplotlib==3.4.3

EXPOSE 8080

####ENTRYPOINT [ "python" , "gaussian_fileparser.py" ]
COPY . .
RUN ["chmod", "+x", "./user_input.sh"]
ENTRYPOINT [ "./run.sh" ]