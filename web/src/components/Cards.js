import React from 'react';
import './Cards.css';
import CardItem from './CardItem';


function Cards() {
    return (
        <div className='cards'>
          <h1>Meet Track-Trend TEAM</h1>
          <div className='cards__container'>
            <div className='cards__wrapper'>
                <ul className='cards__items'>
                    <CardItem
                        src='images/gonzalo.jpeg'
                        text='Team Leader'
                        label='Gonzalo Cordova'
                        //se puede poner un link con path = ''
                    />
                    <CardItem
                        src='images/nuria.jpeg'
                        text='Sub-Team Leader'
                        label='Nuria Cantero'
                    />
                    <CardItem
                        src='images/maria.jpeg'
                        text='IT team'
                        label='Maria Zyatyugina'
                    />
                </ul>
                <ul className='cards__items'>
                    <CardItem
                        src='images/javi.jpeg'
                        text='IT team'
                        label='Javier Mestre'
                    />
                    <CardItem
                        src='images/aina.jpeg'
                        text='Communication and financial manager'
                        label='Aina Mas'
                    />
                    <CardItem
                        src='images/luis.jpeg'
                        text='Unpaid intern'
                        label='Luis Gonzalez'
                    />
                    <CardItem
                    src='images/richi.jpeg'
                    text='Event manager'
                    label='Ricard Tarre'
                    /> 
                </ul>
            </div>
        </div>
    </div>
  );
}

export default Cards;