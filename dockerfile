FROM public.ecr.aws/lambda/python:3.9
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY handler.py ${LAMBDA_TASK_ROOT}
CMD ["handler.handler"]