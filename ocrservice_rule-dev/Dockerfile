FROM python:3.6 AS tesseract-base

RUN apt-get update && \
      apt-get -y install sudo

RUN apt-get install -y libleptonica-dev libtesseract-dev
RUN apt-get install -y automake g++ git libtool libleptonica-dev make pkg-config \
    && apt-get install -y --no-install-recommends asciidoc \
    && apt-get install -y libpango1.0-dev

RUN git clone https://github.com/tesseract-ocr/tesseract.git \
    && cd tesseract \
    && ./autogen.sh \
    && ./configure \
    && make \
    && make install \
    && ldconfig

RUN cd /usr/local/share/tessdata/ && wget https://github.com/tesseract-ocr/tessdata/raw/master/vie.traineddata
RUN cd /usr/local/share/tessdata/ && wget https://github.com/tesseract-ocr/tessdata/raw/master/eng.traineddata

FROM tesseract-base
COPY ./requirements.txt /app/requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 5000
RUN pip install -r requirements.txt
RUN chmod 644 app.py
CMD python app.py
