FROM 046831591010.dkr.ecr.eu-central-1.amazonaws.com/mlesz-base:latest AS builder
COPY requirements.txt .

RUN pip install --user -r requirements.txt


# second unnamed stage
FROM 046831591010.dkr.ecr.eu-central-1.amazonaws.com/mlesz-runner:latest AS runner
WORKDIR /code

COPY --from=builder /root/.local /code/.local
COPY ./src .
RUN printenv
# # add user
# RUN addgroup --system user && adduser --system --no-create-home --group user
# RUN chown -R user:user /code && chmod -R 755 /code
# # # change user from root
# USER user

EXPOSE 80
ENV PYTHONPATH=/code/.local/lib/python3.10/site-packages:$PYTHONPATH

CMD [ "python", "server.py" ] 