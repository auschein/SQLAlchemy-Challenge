{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "\n",
    "import sqlalchemy\n",
    "from sqlalchemy.ext.automap import automap_base\n",
    "from sqlalchemy.orm import Session\n",
    "from sqlalchemy import create_engine, func, inspect\n",
    "\n",
    "from flask import Flask, jsonify\n",
    "import datetime as dt"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "engine = create_engine(\"sqlite:///Resources/hawaii.sqlite\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "base = automap_base()\n",
    "base.prepare(engine, reflect=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "msurmnt= base.classes.measurement\n",
    "stat = base.classes.station"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "session = Session(engine)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "app = Flask(__name__)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/\")\n",
    "def welcome():\n",
    "    \"\"\"List all available api routes.\"\"\"\n",
    "    return (\n",
    "         f\"Avalable Routes:<br/>\"\n",
    "         \n",
    "         f\"/api/v1.0/precipitation<br/>\"\n",
    "         f\"- Dates and Temps from previous year<br/>\"\n",
    "         \n",
    "         f\"/api/v1.0/stations<br/>\"\n",
    "         f\"- Listings of various weather stations <br/>\"\n",
    "\n",
    "         f\"/api/v1.0/tobs<br/>\"\n",
    "         f\"- Listings of temps from previous year<br/>\"\n",
    "\n",
    "         f\"/api/v1.0/<start><br/>\"\n",
    "         f\"- List of maximum, minimum, and avgerage temps for a specific start date<br/>\"\n",
    "        \n",
    "         f\"/api/v1.0/<start>/<end><br/>\"\n",
    "         f\"- List of maximum, minimum, and avgerage temps for a specific start and end date range<br/>\"\n",
    "    )\n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/precipitation\")\n",
    "def precip():\n",
    "\n",
    "    returns = session.query(msurmnt.date, msurmnt.prcp).\\\n",
    "        filter(msurmnt.date <= '2017-12-31').\\\n",
    "        filter(msurmnt.date >= '2017-01-01').all()\n",
    "\n",
    "    total_prcp = []\n",
    "    for result in results:\n",
    "        p_dict = {}\n",
    "        p_dict[\"date\"] = result[0]\n",
    "        p_dict[\"prcp\"] = float(result[1])\n",
    "\n",
    "        total_prcp.append(p_dict)\n",
    "\n",
    "    return jsonify(total_prcp)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/stations\")\n",
    "def stats():\n",
    "    returns = session.query(stat.station).all()\n",
    "    stats_return = list(np.ravel(returns))\n",
    "    return jsonify(stats_return)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/tobs\")\n",
    "def tempobvs():\n",
    "    returns = session.query(msurmnt.date, msurmnt.tobs).\\\n",
    "        group_by(msurmnt.date).\\\n",
    "        filter(msurmnt.date <= '2017-12 31').\\\n",
    "        filter(msurmnt.date >= '2017-01-01').all()\n",
    "\n",
    "    tempobvs_return = list(np.ravel(returns))\n",
    "    return jsonify(tempobvs_return)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app \"__main__\" (lazy loading)\n",
      " * Environment: production\n",
      "   WARNING: Do not use the development server in a production environment.\n",
      "   Use a production WSGI server instead.\n",
      " * Debug mode: off\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)\n",
      "127.0.0.1 - - [08/Oct/2019 21:39:22] \"GET / HTTP/1.1\" 200 -\n",
      "127.0.0.1 - - [08/Oct/2019 21:39:29] \"GET / HTTP/1.1\" 200 -\n"
     ]
    }
   ],
   "source": [
    "@app.route(\"/api/v1.0/<start>\")\n",
    "@app.route(\"/api/v1.0/<start>/<end>\")\n",
    "def start_finish(start=None, end=None):\n",
    "\n",
    "    select = [func.min(msurmnt.tobs), func.avg(msurmnt.tobs), func.max(msurmnt.tobs)]\n",
    "    if not end:\n",
    "        returns= session.query(*select).filter(msurmnt.date >= start).all()\n",
    "        temps = list(np.ravel(returns))\n",
    "        return jsonify(temps)\n",
    "    \n",
    "    returns1 = session.query(*sel).filter(msurmnt.date >= start).filter(msurmnt.date <= end).all()\n",
    "    temps2 = list(np.ravel(returns1))\n",
    "    return jsonify(temps2)\n",
    "\n",
    "if __name__ == '__main__':\n",
    "    app.run()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
